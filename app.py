from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash

import db

app = Flask(__name__)

# Please Ref Appendix for server function
# JWT 비밀키 설정
app.config['JWT_SECRET_KEY'] = 'jungsanghwa'  # 실제로는 안전한 비밀키를 사용하세요 : 뭐라고 하지?
jwt = JWTManager(app)

# 회원 가입 엔드포인트
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if db.search_user_name(username) is not None:
        return jsonify({"message": "User already exists"}), 400

    # 비밀번호 해시화
    hashed_password = generate_password_hash(password)

    db.insert_user(username, hashed_password) # ALERT : UID System 구현해 놓을 것
    return jsonify({"message": "User registered successfully"}), 201


# 로그인 엔드포인트
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user_id = db.get_user_id(username)
    user_password = db.get_user_password(user_id)

    # 사용자가 없거나 비밀번호가 틀린 경우
    if user_password == None or not check_password_hash(user_password, password):
        return jsonify({"message": "Invalid username or password"}), 401

    # 액세스 토큰 생성
    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token), 200


# matchmaking endpoint
@app.route('/matchmaking', methods=['GET']) #Game 종료시 서버 드랍 만들어야됨!!!!!
@jwt_required()
def patchmaking():
    current_user = get_jwt_identity()
    data = db.connect_server(str(db.get_user_id(current_user)))

    return jsonify(arranged_server = data[0], player_count = data[1]), 200

@app.route('/gameover', methods=['GET'])
@jwt_required()
def gameover():
    current_user = get_jwt_identity()
    data = request.get_json()
    target_server_id = data.get('target_server_id')

    db.destroy_server(target_server_id)
    return jsonify(answert="completed!"), 200

if __name__ == '__main__':
    app.run(debug=True)

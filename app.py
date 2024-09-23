from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# JWT 비밀키 설정
app.config['JWT_SECRET_KEY'] = 'jemanParkIsGod'  # 실제로는 안전한 비밀키를 사용하세요
jwt = JWTManager(app)

# 간단한 사용자 데이터베이스
users = {}


# 회원 가입 엔드포인트
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if username in users:
        return jsonify({"message": "User already exists"}), 400

    # 비밀번호 해시화
    hashed_password = generate_password_hash(password)
    users[username] = hashed_password
    return jsonify({"message": "User registered successfully"}), 201


# 로그인 엔드포인트
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user_password = users.get(username)

    # 사용자가 없거나 비밀번호가 틀린 경우
    if not user_password or not check_password_hash(user_password, password):
        return jsonify({"message": "Invalid username or password"}), 401

    # 액세스 토큰 생성
    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token), 200


# 인증이 필요한 보호된 엔드포인트
@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200


if __name__ == '__main__':
    app.run(debug=True)

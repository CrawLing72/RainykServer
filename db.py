import sqlite3
import atexit

con_user = sqlite3.connect("./user.db", check_same_thread=False)
cur_user = con_user.cursor()

# Table existence check
table_check_query = "SELECT name FROM sqlite_master WHERE type='table' AND name='user' "
cur_user.execute(table_check_query)
table_exists = cur_user.fetchone()

if not table_exists:
    cur_user.execute("CREATE TABLE user(UID INTEGER PRIMARY KEY, name TEXT, password TEXT)")
    con_user.commit()


def get_user_id(user_name: str) -> int:
    """get user id by user name"""
    cur_user.execute("SELECT UID FROM user WHERE name=(?)", (user_name,))
    result = cur_user.fetchone()
    if result:
        return result[0]
    return None


def get_user_name(uid: int) -> str:
    """get user name by user id"""
    cur_user.execute("SELECT name FROM user WHERE UID=(?)", (uid,))
    result = cur_user.fetchone()
    if result:
        return result[0]
    return None


def get_user_password(uid: int) -> str:
    """get user password(hashed) by user id"""
    cur_user.execute("SELECT password FROM user WHERE UID=(?)", (uid,))
    result = cur_user.fetchone()
    if result:
        return result[0]
    return None


def search_user_name(user_name: str) -> str:
    """search user by name"""
    cur_user.execute("SELECT name FROM user WHERE name=(?)", (user_name,))
    result = cur_user.fetchone()
    if result:
        return result[0]
    return None


def insert_user(user_name: str, password: str) -> None:
    """insert user into database"""
    cur_user.execute("INSERT INTO user (name, password) VALUES (?, ?)", (user_name, password))
    con_user.commit()


"""------------------------------------------------ Above : USER DB"""


con_sv = sqlite3.connect("./server.db", check_same_thread=False)
cur_sv = con_sv.cursor()

# Table existence check
table_check_query_server = "SELECT name FROM sqlite_master WHERE type='table' AND name='server' "
cur_sv.execute(table_check_query_server)
table_exists_sv = cur_sv.fetchone()

if not table_exists_sv:
    cur_sv.execute("CREATE TABLE server(serverID INTEGER PRIMARY KEY, playerID TEXT, playerCOUNT INTEGER, status TEXT)")
    con_sv.commit()


def create_empty_server():
    """Create Empty Server ('', 0, waiting) """
    cur_sv.execute("INSERT INTO server (playerID, playerCOUNT, status) VALUES (?, ?, ?)", ("", 0, "waiting"))
    con_sv.commit()


def connect_server(player_id: str) -> str:
    """Connect to server and handle datas"""
    cur_sv.execute("SELECT * FROM server WHERE playerCOUNT < 6 AND status != 'onGame'")
    arranging_data = cur_sv.fetchall()[0]

    if not arranging_data:
        create_empty_server()
        return connect_server(player_id)

    arranged_server_id = arranging_data.serverID
    arranged_server_player_id = arranging_data.playerDATA
    arranged_server_player_count = arranging_data.playerCOUNT

    modified_server_player_id = arranged_server_player_id + player_id + "~"

    if arranged_server_player_count == 5:
        cur_sv.execute("UPDATE server SET playerID = (?) WHERE serverID = (?)", (modified_server_player_id, arranged_server_id))
        cur_sv.execute("UPDATE server SET status = (?) WHERE serverID = (?)", ("onGame", arranged_server_id))
        con_sv.commit()
        return "onGame"
    else:
        cur_sv.execute("UPDATE server SET playerID = (?) WHERE serverID = (?)", (arranged_server_id, modified_server_player_id))
        cur_sv.execute("UPDATE server SET playerCOUNT = (?) WHERE serverID = (?)", (++arranged_server_player_count, arranged_server_id))
        con_sv.commit()
        return "waiting"


def get_user_id(server_id: int) -> str:
    """Get user ids by server id"""
    cur_sv.execute("SELECT playerID FROM server WHERE serverID = (?)", (server_id, ))
    server_data = cur_sv.fetchone()

    if not server_data:
        return server_data[0]
    else:
        return "error!"


"""------------------------------------------------ Above : SERVER DB"""


def exit_server():
    con_user.close()
    print("SERVER CLOSED!")


atexit.register(exit_server)


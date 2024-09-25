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

"""------------------------------------------------"""

def exit():
    con_user.close()
    print("SERVER CLOSED!")

atexit.register(exit)


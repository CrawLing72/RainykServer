import sqlite3

con_user = sqlite3.connect("./user.db")
cur_user = con_user.cursor()

cur_user.execute("CREATE TABLE user(UID INTEGER PRIMARY KEY, name TEXT, password TEXT)")
con_user.commit()


def search_user_id(user_name: str) -> int:
    cur_user.execute("SELECT * FROM user WHERE name like ?", str)
    result = cur_user.fetchone()
    print(result)
    return int(result)


def insert_user_id(user_name: str, uid: str) -> None:
    cur_user.execute("INSERT INTO user VALUES (?, ?)", (uid, user_name))
    con_user.commit()





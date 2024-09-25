import sqlite3

con_user = sqlite3.connect("./user.db")
cur_user = con_user.cursor()

cur_user.execute("CREATE TABLE user(UID INTEGER PRIMARY KEY, name TEXT)")
con_user.commit()


def search_user_id(user_name: str):
    cur_user.execute("SELECT * FROM user WHERE name like ?", str)
    result = cur_user.fetchall()
    print(result)


def get_user_id(user_name: str):
    return


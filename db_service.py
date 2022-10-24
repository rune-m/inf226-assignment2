from db_init import initialize_database
from utils import pygmentize
from json import dumps
from markupsafe import escape

conn = initialize_database()

def search_messages(query):
    stmt = f"SELECT * FROM messages WHERE message GLOB ?;"
    result = f"Query: {pygmentize(stmt)}\n"
    c = conn.execute(stmt, (query,))
    rows = c.fetchall()
    result = result + 'Result:\n'
    for row in rows:
        result = f'{result}    {dumps(row)}\n'
    c.close()
    return result

def send_message(sender, message):
    stmt = f"INSERT INTO messages (sender, message) values (?, ?);"
    result = f"Query: {pygmentize(stmt)}\n"
    conn.execute(stmt, (sender, message))
    return result

def get_announcements():
    stmt = f"SELECT author,text FROM announcements;"
    c = conn.execute(stmt)
    anns = []
    for row in c:
        anns.append({'sender':escape(row[0]), 'message':escape(row[1])})
    return {'data':anns}

def get_credentials(username):
    stmt = f"SELECT username, password, salt FROM users WHERE username GLOB ?;"
    c = conn.execute(stmt, (username,))
    for row in c:
      return {'username': row[0], 'password': row[1], 'salt': row[2]}

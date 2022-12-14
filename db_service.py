from db_init import initialize_database
from password_utils import hash_password
from utils import pygmentize
from json import dumps
from markupsafe import escape

conn = initialize_database()

def search_messages(query, user_id):
    stmt = f"SELECT * FROM messages WHERE message GLOB ? AND (sender = ? OR recipient = ? OR recipient = '*');"
    result = f"Query: {pygmentize(stmt)}\n"
    c = conn.execute(stmt, (query, user_id, user_id))
    rows = c.fetchall()
    result = result + 'Result:\n'
    for row in rows:
        result = f'{result}    {dumps(row)}\n'
    c.close()
    return result

def send_message(sender, message, recipient, reply_to):
    c = conn.cursor()
    stmt = f"INSERT INTO messages (sender, message, recipient, reply_to, timestamp) values (?, ?, ?, ?, datetime('now', 'localtime'));"
    result = f"Query: {pygmentize(stmt)}\n"
    c.execute(stmt, (sender, message, recipient, reply_to))
    return result

def get_all_messages(userId):
    c = conn.cursor()
    stmt = f"SELECT sender, recipient, reply_to, message, timestamp, id FROM messages WHERE sender = ? OR recipient = ? OR recipient = '*';"
    c = c.execute(stmt, (userId, userId))
    anns = []
    for row in c:
        anns.append({'sender':escape(row[0]), 'recipient':escape(row[1]), 'reply_to': escape(row[2]), 'message': escape(row[3]), 'timestamp': escape(row[4]), 'id': escape(row[5])})
    return {'data':anns}

def get_message(id, userId):
    c = conn.cursor()
    stmt = f"SELECT sender, recipient, reply_to, message FROM messages WHERE id = ? AND (sender = ? OR recipient = ? OR recipient = '*');"
    c = c.execute(stmt, (id, userId, userId))
    for row in c: 
        return {'sender':escape(row[0]), 'recipient':escape(row[1]), 'reply_to': escape(row[2]), 'message': escape(row[3])}

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

def create_user(username, password):
    (hash, salt) = hash_password(password, salt=None)
    c = conn.cursor()
    stmt = f"INSERT INTO users (username, password, salt, token) values (?, ?, ?, ?);"
    c.execute(stmt, (username, hash, salt, 'token?'))
    return
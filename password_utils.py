import bcrypt

def hash_password(password: str, salt: str):
    if salt == None or salt == '':
        salt = bcrypt.gensalt()
    else:
        salt = salt.encode('utf-8')
    pass_encoded = password.encode('utf-8')
    hashed = bcrypt.hashpw(pass_encoded, salt)
    return (hashed, salt)

def check_password(correct_hash, password, salt):
    return hash_password(password, salt)[0] == correct_hash.encode('utf-8')

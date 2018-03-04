import hashlib

import db_setup
import encryption


def main():
    password = 's3krit pa55wort!'
    key = hashlib.sha256(password).digest()
    bad_key = hashlib.sha256('not password').digest()

    print("Encrypting existing database")
    encryption.encrypt(key, 'passwords.db', 'passwords.db.enc')

    print("Decrypting just-encrypted database")
    encryption.decrypt(key, 'passwords.db.enc', 'decrypted-passwords.db')
    print("Connecting to decrypted database.")
    conn = db_setup.connect_to_db('decrypted-passwords.db')
    conn.close()

    print("Decrypting database with bad key.")
    encryption.decrypt(bad_key, 'passwords.db.enc', 'bad-decrypted-passwords.db')
    print("Connecting to garbage database.")
    conn = db_setup.connect_to_db('bad-decrypted-passwords.db')
    conn.close()


if __name__ == "__main__":
    main()

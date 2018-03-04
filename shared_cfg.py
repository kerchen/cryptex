import threading

cv = threading.Condition()

db_filename = "\home\pi\cryptex.db"
encrypted_db_filename = db_filename + ".enc"

db_conn = None


import sqlite3


def get_db():
    db = sqlite3.connect('sqlite_db',detect_types=sqlite3.PARSE_DECLTYPES)
    db.row_factory=sqlite3.Row

    return db


def close_db(db):
    if db is not None:
        db.close()

def init_db():
    db=get_db()
    print(db)
    with open("schema.sql",'rb') as f:
        db.executescript(f.read().decode("utf8"))
    db.commit()   
    close_db(db)
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    print("Initialized the database.")
    

  
from sqlalchemy import create_engine
from config import username, password, hostname, database


# Sample query of the database


def login_request():
    '''
    App login
    '''

    engine = create_engine(f"postgresql+psycopg2://{username}:{password}@{hostname}/{database}")

    query = '''
    Select * FROM authenticate LIMIT 1;
    '''

    conn = engine.connect()

    data = conn.execute(query).fetchall()

    login_id, first_name, last_name, username, password_hash = [], [], [], [], []

    submission_dict = {
        "login_id": row[0],
        "first_name": row[1],
        "last_name": row[2],
        "username": row[3],
        "password_hash": row[4]
    }  

    conn.close()
    engine.dispose()

    return submission_dict

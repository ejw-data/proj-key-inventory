from config import username, password, hostname, database

# Databases
path = {
    "key_inventory": f"postgresql+psycopg2://{username}:{password}@{hostname}/{database}"
    }

import os

local_user = os.environ.get("PG_USER")
local_pass = os.environ.get("PG_PASS")
local_host = os.environ.get("PG_HOST")
local_port = os.environ.get("PG_PORT")
local_db_name = os.environ.get("PG_DATABASE")
gcp_user = os.environ.get("CLOUDSQL_USER")
gcp_pass = os.environ.get("CLOUDSQL_PASSWORD")
gcp_connection = os.environ.get("CLOUDSQL_CONNECTION_NAME")
gcp_db_name = os.environ.get("CLOUDSQL_DATABASE_NAME")
gcp_host = os.environ.get("CLOUDSQL_HOST")

# Databases
path = {
    "local_db": f"postgresql+psycopg2://{local_user}:{local_pass}@{local_host}:{local_port}/{local_db_name}",
    "gcp_db": f"postgresql://{gcp_user}:{gcp_pass}@{gcp_host}/{gcp_db_name}"
}

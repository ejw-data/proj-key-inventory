from config import local_user, local_pass, local_host, local_port, local_db_name, gcp_user, gcp_pass, gcp_host, gcp_port, gcp_db_name

# Databases
path = {
    "local_db": f"postgresql+psycopg2://{local_user}:{local_pass}@{local_host}:{local_port}/{local_db_name}",
    "gcp_db": f"postgresql://{gcp_user}:{gcp_pass}@{gcp_host}/{gcp_db_name}",
}

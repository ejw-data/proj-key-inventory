from sqlalchemy import create_engine, text, and_, or_
from flask_login import current_user
import json
from config import username, password, hostname, database
from models import Users, Titles, Roles, KeyOrders, Requests

# Sample query of the database


def get_access_code(room_list):
    """
    Retrieve key access code
    """
    # replace connection with 'path' from db_paths.py - in attempt to reduce duplications
    engine = create_engine(
        f"postgresql+psycopg2://{username}:{password}@{hostname}/{database}"
    )

    # values = ["B24010101", "B24020102", "B24020101"]
    tuple_list = tuple([(i,) for i in room_list])
    query_test = str(tuple_list).replace(",)", ")")[1:-1]

    query = rf"""
    with temp_matrix as (
	SELECT access_code_id::text, space_number_id, 1 as Truth
	FROM access_pairs
	order by 1,2
    ),
    room_selections as (
        Select column1 as rooms FROM (VALUES {query_test}) as room
    ),
    possibilities as (
    select distinct tm.access_code_id
    from temp_matrix tm
    where tm.space_number_id in (Select rooms from room_selections)
    ),
    all_combinations as (
    select t.space_number_id, t.access_code_id, p.access_code_id is not null as contains_any
    from temp_matrix t
    Left join possibilities p on t.access_code_id = p.access_code_id
    ),
    true_combinations as (
        Select *
        From all_combinations
        WHERE contains_any = true
    ),
    not_possibilities as (
    select distinct tc.access_code_id
    from true_combinations tc
    where tc.space_number_id not in (Select rooms from room_selections)
    ),
    show_mismatches as (
    select tco.space_number_id, tco.access_code_id, np.access_code_id is not null as not_exact
    from true_combinations tco
    Left join not_possibilities np on tco.access_code_id = np.access_code_id
    ),
    remove_mismatches as (
        select *
        from show_mismatches
        where not_exact = false
    )
    Select access_code_id, count(access_code_id)
    From remove_mismatches
    Group by access_code_id
    Having count(access_code_id) = (Select count(rooms) FROM room_selections);

    """
    # print("Query", query)

    conn = engine.connect()

    results = conn.execute(text(query)).fetchall()

    conn.close()
    engine.dispose()

    # check this if it is an empty list and return zero
    # is there a case when this returns mutliple numbers? - I don't think so
    # make this function return only a integer and if more than one integer 
    # is returned then create error handling logic
    # I can simplify this to not include the list comprehension
    print(results)
    data = [int(i[0]) for i in results]
    if len(data[0]) == 0:
        output = 0
    else:
        output = data[0]

    return output


def get_profile():
    login_user_id = current_user.get_id()

    profile = (
        Users.query.with_entities(
            Users.first_name,
            Users.last_name,
            Users.email,
            Titles.title,
            Roles.user_role,
        )
        .filter_by(user_id=login_user_id)
        .join(Titles, Titles.title_id == Users.title_id)
        .join(Roles, Roles.role_id == Users.role_id)
        .first()
    )

    assigned_keys = (
        Requests.query.filter(Requests.user_id == login_user_id)
        .filter(or_(Requests.request_status_id == 6, Requests.request_status_id == 7))
        .count()
    )

    pending_keys = (
        Requests.query.filter(Requests.user_id == login_user_id)
        .filter(and_(Requests.request_status_id < 6, Requests.request_status_id != 3))
        .count()
    )
    data = {
        "first_name": profile.first_name.title(),
        "last_name": profile.last_name.title(),
        "email": profile.email,
        "title": profile.title.title(),
        "role": profile.user_role.title(),
        "assigned_keys": assigned_keys,
        "pending_keys": pending_keys,
    }

    return data

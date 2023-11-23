from sqlalchemy import create_engine, text
from config import username, password, hostname, database


# Sample query of the database


def get_access_code(room_list):
    """
    Retrieve key access code
    """

    engine = create_engine(
        f"postgresql+psycopg2://{username}:{password}@{hostname}/{database}"
    )

    # values = ["B24010101", "B24020102", "B24020101"]
    tuple_list = tuple([(i,) for i in room_list])
    query_test = str(tuple_list).replace(",)", ")")

    query = fr"""
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
    
    conn = engine.connect()

    results = conn.execute(text(query)).fetchall()

    conn.close()
    engine.dispose()

    data = [int(i[0]) for i in results]

    return data

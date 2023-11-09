-- Sample table structure
CREATE TABLE YourTable (
    access_code text,
    room_number text
);
-- Insert sample data
INSERT INTO YourTable (access_code, room_number)
VALUES
    ('Code1', 'Room1'),
    ('Code1', 'Room2'),
    ('Code2', 'Room2'),
    ('Code3', 'Room3');

-- Enable the tablefunc extension
CREATE EXTENSION IF NOT EXISTS tablefunc;

-- Create a new table with the pivoted data
SELECT * FROM crosstab(
	'SELECT access_code, room_number, 1 as Truth FROM YourTable order by 1,2')
	as YourTable (room_number text, rm1 int, rm2 int, rm3 int);
	
-- Find access codes given list of rooms - NOT CORRECT FOR room_number 2
SELECT * FROM crosstab(
	'SELECT access_code_id::text, space_number_id, 1 as Truth FROM access_pairs order by 1,2')
	as access_pairs (room_number text, rm1 int, rm2 int, rm3 int);
	
-- Find access codes given list of rooms
select * from crosstab (
    'select access_code_id::text, space_number_id, 1 from access_pairs group by 1,2 order by 1,2',
    'select distinct space_number_id from access_pairs order by 1'
    )
    as newtable (
    access_code_id varchar,_col1 integer,_col2 integer,_col3 integer
    );	
	
	
string_agg(select distinct space_number_id from access_pairs order by 1, " text,")
	
-- Simpler version using pgSQL
DO $$ 
DECLARE 
	value_query text := 'select access_code_id::text, space_number_id, 1 from access_pairs group by 1,2 order by 1,2';
	cat_query text := 'select distinct space_number_id from access_pairs order by 1';
BEGIN
DROP TABLE IF EXISTS temp_pivot;
EXECUTE(SELECT
  'CREATE TABLE temp_pivot AS SELECT * FROM crosstab(
   ''$value_query'', ''$cat_query'') AS ct (rn text, "'
   || string_agg($cat_query, '" text,"') || '" text);'
   FROM $cat_query
); 
END $$;
SELECT * FROM temp_pivot;







-- Complicated version
CREATE OR REPLACE FUNCTION field_values_ct ()
 RETURNS VOID AS $$
DECLARE rec RECORD;
DECLARE str text;
BEGIN
str := 'room_number text,';
   -- looping to get column heading string
   FOR rec IN SELECT DISTINCT space_number_id
        FROM access_pairs
        ORDER BY space_number_id
    LOOP
    str :=  str || '"' || rec.space_number_id || '" text' ||',';
    END LOOP;
    str:= substring(str, 0, length(str));

    EXECUTE 'CREATE EXTENSION IF NOT EXISTS tablefunc;
    DROP TABLE IF EXISTS temp_issue_fields;
    CREATE TABLE temp_issue_fields AS
    SELECT *
    FROM crosstab(''SELECT access_code_id::text, space_number_id, 1 as Truth FROM access_pairs order by 1,2'')
		as access_pairs ('|| str ||')';
END;
$$ LANGUAGE plpgsql;

Select * FROM field_values_ct()



CREATE TEMPORARY TABLE temp_matrix AS
SELECT access_code_id::text, space_number_id, 1 as Truth 
FROM access_pairs 
order by 1,2;

Select * FROM temp_matrix;


create or replace function pivotcode (tablename varchar, rowc varchar, colc varchar, cellc varchar, celldatatype varchar) returns varchar language plpgsql as $$
declare
    dynsql1 varchar;
    dynsql2 varchar;
    columnlist varchar;
begin
    -- 1. retrieve list of column names.
    dynsql1 = 'select string_agg(distinct ''_''||'||colc||'||'' '||celldatatype||''','','' order by ''_''||'||colc||'||'' '||celldatatype||''') from '||tablename||';';
    execute dynsql1 into columnlist;
    -- 2. set up the crosstab query
    dynsql2 = 'select * from crosstab (''select '||rowc||','||colc||','||cellc||' from '||tablename||' group by 1,2 order by 1,2'',''select distinct '||colc||' from '||tablename||' order by 1'') as newtable ('||rowc||' varchar,'||columnlist||');';
    execute dynsql2;
end;
$$;

DO $$
BEGIN
	PERFORM pivotcode('temp_matrix','access_code_id','space_number_id','max(truth)','integer');
END $$;






DROP FUNCTION pivotcode(character varying,character varying,character varying,character varying,character varying)

create or replace function pivotcode (tablename varchar, rowc varchar, colc varchar, cellc varchar, celldatatype varchar) returns void language plpgsql as $$
declare
    dynsql1 varchar;
    dynsql2 varchar;
    columnlist varchar;
begin
    -- 1. retrieve list of column names.
    dynsql1 = 'select string_agg(distinct '||colc||'||'' '||celldatatype||''','','' order by '||colc||'||'' '||celldatatype||''') from '||tablename||';';
    execute dynsql1 into columnlist;
    -- 2. set up the crosstab query
    dynsql2 = 'CREATE TEMPORARY TABLE temp_pivot AS select * from crosstab (''select '||rowc||','||colc||','||cellc||' from '||tablename||' group by 1,2 order by 1,2'',''select distinct '||colc||' from '||tablename||' order by 1'') as newtable ('||rowc||' varchar,'||columnlist||');';
    execute dynsql2;
end;
$$;

CREATE TEMPORARY TABLE temp_matrix AS
SELECT access_code_id::text, space_number_id, 1 as Truth 
FROM access_pairs 
order by 1,2;

DO $$
BEGIN
    PERFORM pivotcode('temp_matrix', 'access_code_id', 'space_number_id', 'max(truth)', 'integer');
END $$;

SELECT * FROM temp_pivot

Select *
FROM temp_pivot
WHERE (b24010101 = 1) and (b24020101 = 1);



SELECT * FROM temp_matrix;
-- can i do this without creating the view and without the lengthy WHERE clause
WITH to_check (tags) as (
	VALUES ('B24010101'), ('B24020101')
)
SELECT tc.tags,
	exists(SELECT t.access_code_id FROM temp_matrix t WHERE t.space_number_id = tc.tags) as tag_exists
FROM to_check tc;

Select * 
FROM temp_matrix




-- Query shows that it contains all
with room_selections as (
	Select column1 as rooms FROM (VALUES ('B24010101'), ('B24020102'), ('B24020101')) as room
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
Having count(access_code_id) = (Select count(rooms) FROM room_selections)









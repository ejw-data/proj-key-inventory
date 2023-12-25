-- -----------------------------------------------------------
--
--  Create key access code lookup table in SQL by manually entering column names
--
-- ------------------------------------------------------------

-- Enable the tablefunc extension to use crosstab
CREATE EXTENSION IF NOT EXISTS tablefunc;

	
-- Find access codes given list of rooms
select * from crosstab (
    'select access_code_id::text, space_number_id, 1 from access_pairs group by 1,2 order by 1,2',
    'select distinct space_number_id from access_pairs order by 1'
    ) as newtable (access_code_id varchar,_col1 integer,_col2 integer,_col3 integer);	
	
	

-- -----------------------------------------------------------
--
--  Create key access code lookup table in SQL dynamically
--
-- ------------------------------------------------------------

-- drop existing structures
DROP FUNCTION pivotcode(character varying,character varying,character varying,character varying,character varying);
DROP TABLE IF EXISTS temp_pivot;
DROP TABLE IF EXISTS temp_matrix;

-- create correctly structured table
-- CREATE TEMPORARY TABLE temp_matrix AS
-- SELECT access_code_id::text, space_number_id, 1 as Truth 
-- FROM access_pairs 
-- order by 1,2;

CREATE VIEW temp_matrix AS
SELECT access_code_id::text, space_number_id, 1 as Truth 
FROM access_pairs 
order by 1,2;


-- view table
Select * FROM temp_matrix;

-- create function that writes the sql query dynamically
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

-- activate extenstion that includes crosstab
 create extension tablefunc;

-- execute the function
DO $$
BEGIN
    PERFORM pivotcode('temp_matrix', 'access_code_id', 'space_number_id', 'max(truth)', 'integer');
END $$;

-- view results
SELECT * FROM temp_pivot

-- use table in to filter results
Select *
FROM temp_pivot
WHERE (b24010101 = 1) and (b24020101 = 1);



-- -----------------------------------------------------------
--
--  Query to find unique access code given list of rooms
--
-- ------------------------------------------------------------

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


-- Notes -------------------------------------------------------

-- Dynamic SQL produces a table (see above).  The key parts of this pgSQL code is that the
-- 1.  function returns void 
-- 2.  second query roduces a temporary table (CREATE TEMPORARY TABLE temp_pivot AS)
-- 3.  second query is set to execute 

-- To printout the sql query and not display the table then the following
-- need to be changed.
-- 1.  function returns varchar
-- 2.  second query does not include 'CREATE TEMPORARY TABLE temp_pivot AS'
-- 3.  second query is not executed but returned






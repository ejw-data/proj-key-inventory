-- Logic 
-- create function that is triggered by status_code = 2 (approved)
CREATE OR REPLACE FUNCTION log_key_order()
  RETURNS TRIGGER 
  LANGUAGE PLPGSQL
  AS
$$
BEGIN
	IF NEW.status_code = 2 THEN
		 INSERT INTO key_orders (request_id, access_code_id)
		 VALUES(OLD.request_id, OLD.access_code_id);
	END IF;

	RETURN NEW;
END;
$$;

CREATE TRIGGER request_approved_create_order
  AFTER UPDATE
  ON requests
  FOR EACH ROW
  EXECUTE PROCEDURE log_key_order();


-- check inventory table

CREATE OR REPLACE FUNCTION update_key_order()
  RETURNS TRIGGER 
  LANGUAGE PLPGSQL
  AS
$$
declare
    dynsql;
    dynsql2;
BEGIN
    dynsql = 'SELECT count(access_code_id) FROM key_inventory
              WHERE (access_code_id = xxx) AND (key_status_id = 1)  '
    execute dynsql into id_count;
END
BEGIN

    dynsql2 = ' SELECT request_id, access_code_id, key_copy) FROM key_inventory
              WHERE (key_number = xxx) AND (key_status_id = 1)
              ORDER BY key_number ASC 
              LIMIT 1  '
    execute dynsql2 into id_selected;
END
	IF id_count > 0 THEN
    -- select id and 

		 UPDATE key_inventory
     SET OLD.access_code_id = 2
     WHERE OLD.request_id = dynsql[0];

    -- date_stransferred is auto added and date_returned is null
     INSERT INTO key_inventory (request_id, access_code_id, key_copy, key_status_id)
     VALUES (OLD.request_id, dynsql[1], dynsql[2], 1);

	END IF;

	RETURN NEW;
END;
$$;
CREATE TRIGGER set_key_order_status()
  AFTER INSERT
  ON key_orders
  FOR EACH ROW
  EXECUTE PROCEDURE update_key_order();



-- Example
CREATE OR REPLACE FUNCTION dynamic_column_name(_col_name text, OUT return_value text)
  RETURNS text
  LANGUAGE plpgsql AS
$func$
BEGIN
   EXECUTE format('SELECT %I FROM customer WHERE id = 1', _col_name)
   INTO return_value;
END
$func$;
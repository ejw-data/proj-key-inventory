-- PostgreSQL Trigger Logic 

---------------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------------
-- create function that is triggered by the update of requests table with a request_status_id = 2 (approved) 
-- and inserts part of the record into the key_orders

CREATE OR REPLACE FUNCTION insert_key_order()
  RETURNS TRIGGER 
  LANGUAGE PLPGSQL
  AS
$$
BEGIN
	IF (NEW.request_status_id <> OLD.request_status_id) AND (NEW.request_status_id = 2) THEN
		 INSERT INTO key_orders (request_id, access_code_id)
		 VALUES(OLD.request_id, OLD.access_code_id);
	END IF;

	RETURN NEW;
END;
$$;

CREATE TRIGGER create_key_order
  AFTER UPDATE
  ON requests
  FOR EACH ROW
  EXECUTE PROCEDURE insert_key_order();



-----------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------
-- create function that is triggered by the update of the status column of the keys_created table. 
-- upon this update, the key_inventory table is updated and the key_orders table updated
CREATE OR REPLACE FUNCTION update_key_order()
  RETURNS TRIGGER 
  LANGUAGE PLPGSQL
  AS
$$
BEGIN
	IF (NEW.fabrication_status_id <> OLD.fabrication_status_id) AND (NEW.fabrication_status_id = 3)  THEN

		-- Insert new key record into key inventory
		 INSERT INTO key_inventory (request_id, access_code_id, key_copy, key_status_id)
		 VALUES(NEW.request_id, NEW.access_code_id, NEW.key_copy, 1);  -- key_status_id = ISSUED
	
		-- Updated key_order status  
		 UPDATE key_orders
		 SET order_status_id = 3  -- WAITING FOR DELIVERY
		 WHERE request_id = OLD.request_id;
	END IF;

	RETURN NEW;
END;
$$;

-- create a trigger that updates the key_inventory and key_orders table
CREATE TRIGGER update_key_order_status
  AFTER UPDATE
  ON keys_created
  FOR EACH ROW
  EXECUTE PROCEDURE update_key_order();


-----------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------
-- create function that is triggered by the update of the status column of the key_orders table. 
-- 
CREATE OR REPLACE FUNCTION update_requests()
  RETURNS TRIGGER 
  LANGUAGE PLPGSQL
  AS
$$
BEGIN
	IF NEW.order_status_id = 1 THEN   -- READY FOR PICKUP

		-- Updated request status  
		 UPDATE requests
		 SET  request_status_id = 5 -- KEY READY FOR PICKUP
		 WHERE request_id = OLD.request_id;
	END IF;

	IF NEW.order_status_id = 4 THEN   -- PICKUP COMPLETE

		-- Updated request status  
		 UPDATE requests
		 SET  request_status_id = 6 -- KEY ASSIGNED
		 WHERE request_id = OLD.request_id;
	END IF;

	RETURN NEW;
END;
$$;
-- create a trigger that updates the key_inventory table
CREATE TRIGGER update_request_status
  AFTER UPDATE
  ON key_orders
  FOR EACH ROW
  EXECUTE PROCEDURE update_requests();



-----------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------
-- create function that is triggered by the insertion of a row into the keys_orders table
-- and does one of two things:  1) checks key_inventory for a matching access_code_id table and if available
-- updates the key_status to being assigned and updates the status of the keys_orders table
-- OR 2) checks key_inventory  for a matching access_code_id and if NOT available
-- inserts info to the keys_created table and updates the keys_orders table  

CREATE OR REPLACE FUNCTION check_for_key()
  RETURNS TRIGGER 
  LANGUAGE PLPGSQL
  AS
$$
DECLARE
	record key_inventory%rowtype;
BEGIN  

SELECT * INTO record
	FROM key_inventory 
	WHERE (key_status_id = 2)   -- key_status = INVENTORY
	ORDER BY date_transferred ASC
	LIMIT 1;

IF EXISTS (
	SELECT
	FROM key_inventory 
	WHERE (key_status_id = 2)   -- key_status = INVENTORY
	ORDER BY date_transferred ASC
	LIMIT 1)
THEN
	-- update existing available key to be unavailable
	UPDATE key_inventory
	SET key_status_id = 7,    -- status = TRANSFERRED	
		date_transferred = NOW()
	WHERE request_id = record.request_id;
	
 	-- create new key record with reassigned key
 	INSERT INTO key_inventory (request_id, key_copy, access_code_id, key_status_id)
	VALUES (NEW.request_id, record.key_copy, record.access_code_id, 3);
	
	-- update key order status
	NEW.order_status_id := 3;  -- status = WAITING FOR DELIVERY
	
ELSE
	-- add key request to keyshop
	INSERT INTO keys_created (request_id, access_code_id)
	VALUES (NEW.request_id, NEW.access_code_id);

	-- update key_order status
	NEW.order_status_id := 2;  -- order_status = WAITING FOR FABRICATION
	
END IF;

-- insert record with parameters of NEW
RETURN NEW;

END;
$$;

-- create trigger to insert values when key_orders table has new record
CREATE TRIGGER check_key_status
  BEFORE INSERT
  ON key_orders
  FOR EACH ROW
  EXECUTE PROCEDURE check_for_key();

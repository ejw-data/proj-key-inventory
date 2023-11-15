DROP TABLE IF EXISTS key_inventory;
DROP TABLE IF EXISTS keys_created;
DROP TABLE IF EXISTS key_status;
DROP TABLE IF EXISTS requests CASCADE;
DROP TABLE IF EXISTS access_pairs;
DROP TABLE IF EXISTS access_codes CASCADE;
DROP TABLE IF EXISTS rooms CASCADE;
DROP TABLE IF EXISTS room_amenities;
DROP TABLE IF EXISTS room_classification CASCADE;
DROP TABLE IF EXISTS key_orders CASCADE;
DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS titles;
DROP TABLE IF EXISTS roles;
DROP TABLE IF EXISTS access_approvers CASCADE;
DROP TABLE IF EXISTS approval_status;
DROP TABLE IF EXISTS approver_zones;
DROP TABLE IF EXISTS buildings CASCADE;
DROP TABLE IF EXISTS fabrication_status;
DROP TABLE IF EXISTS authentication; 


-- USERS ------------------------------------------------------
CREATE TABLE titles (
	title_id SERIAL PRIMARY KEY,
	title VARCHAR UNIQUE NOT NULL
);

INSERT INTO titles (title)
VALUES ('undergraduate student'),
		('graduate student'),
		('staff'),
		('faculty'),
		('building manager'),
		('department head'),
		('dean'),
		('senior administration'),
		('facilities');

CREATE TABLE roles (
	role_id SERIAL PRIMARY KEY,
	user_role VARCHAR
);

INSERT INTO roles (user_role)
VALUES ('requester'),
		('approver'),
		('administrator');

CREATE TABLE users (
	user_id SERIAL PRIMARY KEY,
	first_name VARCHAR,
	last_name VARCHAR,
	title_id INT REFERENCES titles (title_id),
	role_id INT REFERENCES roles (role_id),
	email VARCHAR UNIQUE
);

INSERT INTO users (first_name, last_name, title_id, role_id, email)
VALUES ('erin', 'wills', 1, 1, 'ew@mysite.com'),
		('will', 'wright', 1, 1, 'ww@mysite.com'),
		('andrew', 'ng', 1, 1, 'an@mysite.com'),
		('bob', 'turtle', 5, 3, 'bt@mysite.com'),
		('jake', 'powers', 9, 3, 'jp@mysite.com');
		

CREATE TABLE access_approvers (
	access_approver_id SERIAL PRIMARY KEY,
	approver_id INT REFERENCES users (user_id),
	role_approved_by VARCHAR,
	date_approved TIMESTAMP NOT NULL DEFAULT NOW(),
	date_removed TIMESTAMP
);

INSERT INTO access_approvers (approver_id, role_approved_by)
VALUES (4, 9);

-- LOGIN _____________________________________________________


-- change so that primary key is also foreign key to users (user_id), keep only username, password_hash
CREATE TABLE authentication (
	id INT PRIMARY KEY REFERENCES users (user_id),
	username VARCHAR,
	password_hash VARCHAR
);

INSERT INTO authentication (login_id, username, password_hash)
VALUES (1, 'ejwadmin', 'alf344t4090j0aojfsfa');

-- SPACE & GRANTED APPROVAL ------------------------------------------------------------

CREATE TABLE buildings (
	building_number INT PRIMARY KEY,
	building_name VARCHAR,
	building_description VARCHAR
);

INSERT INTO buildings (building_number, building_name, building_description)
VALUES (24, 'Chemistry', 'Chemistry Department Research Space');


CREATE TABLE approver_zones (
	building_number INT REFERENCES buildings (building_number),
	access_approver_id INT REFERENCES access_approvers (access_approver_id),
	PRIMARY KEY (building_number, access_approver_id)
);

INSERT INTO approver_zones (building_number, access_approver_id)
VALUES (24, 1);

CREATE TABLE room_classification (
	room_type_id INT PRIMARY KEY,
	room_type VARCHAR
);

INSERT INTO room_classification (room_type_id, room_type)
VALUES (201, 'private office'),
		(205, 'conference room'),
		(210, 'classroom'),
		(220, 'shared office');

CREATE TABLE rooms (
	space_number_id VARCHAR PRIMARY KEY,
	building_number INT REFERENCES buildings (building_number),
	floor_number INT,
	wing_number INT,
	room_number INT,
	room_type INT REFERENCES room_classification (room_type_id)
);

INSERT INTO rooms (space_number_id, building_number, floor_number, wing_number, room_number, room_type)
VALUES ('B24010101', 24, 01, 01, 01, 210),
		('B24020101', 24, 02, 01, 01, 201),
		('B24020102', 24, 02, 01, 02, 220);


CREATE TABLE room_amenities (
	space_number_id VARCHAR PRIMARY KEY REFERENCES rooms (space_number_id),
	room_projector BOOL,
	room_seating INT
); 

INSERT INTO room_amenities (space_number_id, room_projector, room_seating)
VALUES ('B24010101', TRUE, 50),
		('B24020101', FALSE, 1),
		('B24020102', FALSE, 4);


-- ACCESS ASSIGNMENT -------------------------------------------------------------------
-- changed access_code to access_code_id - need to consider the effect
CREATE TABLE access_codes (
	access_code_id SERIAL PRIMARY KEY,
	access_description VARCHAR,
	created_by VARCHAR,
	authorized_by VARCHAR,
	created_on TIMESTAMP NOT NULL DEFAULT NOW()
);

INSERT INTO access_codes (access_description, created_by, authorized_by)
VALUES ('Classroom', 'ejw', 'T. Bundy'),
		('Faculty Office and Suite', 'ejw', 'Prof. Andrews'),
		('Front Suite Only', 'ejw', 'Prof. Andrews');

-- APPROVAL PROCESS ------------------------------------------------------------

CREATE TABLE approval_status (
	status_code SERIAL PRIMARY KEY,
	status_code_name VARCHAR
);

INSERT INTO approval_status (status_code_name)
VALUES ('REQUEST SUBMITTED'),
		('REQUEST APPROVED'),
		('REQUEST REJECTED'),
		('KEY CREATED'),
		('KEY READY FOR PICKUP'),
		('KEY ASSIGNED');

-- requests table:  request_id, user_id, space, approver, status, dates, reasoning
-- logic updates record
-- logic on update adds record to key_owner table the deletes record
CREATE TABLE requests (
	request_id SERIAL PRIMARY KEY,
	user_id INT,
	space_number_id VARCHAR,
	building_number INT,
	access_approver_id INT,
	access_code_id INT REFERENCES access_codes (access_code_id),
	status_code INT REFERENCES approval_status (status_code),
	request_date TIMESTAMP NOT NULL DEFAULT NOW(),
	approved_date TIMESTAMP,
	approved BOOL DEFAULT FALSE,
	approval_comment VARCHAR,
	rejection_comment VARCHAR,
	FOREIGN KEY (building_number, access_approver_id) REFERENCES approver_zones (building_number, access_approver_id)
);

-- Logic 
-- create function that is triggered by status_code = 2 (approved)
CREATE OR REPLACE FUNCTION log_key_order()
  RETURNS TRIGGER 
  LANGUAGE PLPGSQL
  AS
$$
BEGIN
	IF NEW.status_code = 2 THEN
		 INSERT INTO key_orders (transaction_id, access_code_id)
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
  

-- cannot make access_code_id a FK since it is not a primary key in requests table
-- instead of making a constraint, I will add this information via a trigger function
CREATE TABLE key_orders (
	transaction_id INT PRIMARY KEY REFERENCES requests (request_id),
	access_code_id INT
);

		
-- -- Need to add logic so access code is programatically obtained
-- INSERT INTO key_orders (transaction_id, access_code_id)
-- VALUES (1, 3),
-- 		(2, 1),
-- 		(3, 2),
-- 		(4, 2),
-- 		(5, 2);


CREATE TABLE access_pairs (
	access_code_id INT REFERENCES access_codes (access_code_id),
	space_number_id VARCHAR REFERENCES rooms (space_number_id),
	PRIMARY KEY (access_code_id, space_number_id) 
);

SELECT * FROM access_codes;

INSERT INTO access_pairs (access_code_id, space_number_id)
VALUES (1, 'B24010101'),
		(2, 'B24020101'),
		(2, 'B24020102'),
		(3, 'B24010101'),
		(3, 'B24020101'),
		(3, 'B24020102');
		
CREATE TABLE fabrication_status (
	fabrication_status_id SERIAL PRIMARY KEY,
	fabrication_status VARCHAR
);		

INSERT INTO fabrication_status (fabrication_status)
VALUES ('IN QUEUE'),
		('SCHEDULED'),
		('COMPLETED');

CREATE TABLE keys_created (
	key_number INT,
	key_copy INT,
	access_code_id INT REFERENCES access_codes (access_code_id),
	fabrication_status_id INT DEFAULT 1 REFERENCES fabrication_status (fabrication_status_id),
	PRIMARY KEY (key_number, key_copy)
);

INSERT INTO keys_created (key_number, key_copy, access_code_id, fabrication_status_id)
VALUES (43221, 1, 3, 3),
		(56432, 1, 1, 3),
		(34523, 1, 2, 3),
		(46363, 2, 2, 3),
		(59873, 3, 2, 3);


CREATE TABLE key_status (
	key_status_id SERIAL PRIMARY KEY,
	key_status VARCHAR 
);

INSERT INTO key_status (key_status)
VALUES ('ISSUED'),
		('INVENTORY'),
		('ASSIGNED FOR PICKUP'),
		('BROKEN'),
		('LOST');

CREATE TABLE key_inventory (
	transaction_id INT REFERENCES key_orders (transaction_id),
	key_number INT,
	key_copy INT,
	key_status_id INT REFERENCES key_status (key_status_id),
	date_transferred TIMESTAMP NOT NULL DEFAULT NOW(),
	date_returned TIMESTAMP,
	PRIMARY KEY (transaction_id, key_number, key_copy),
	FOREIGN KEY (key_number, key_copy) REFERENCES keys_created (key_number, key_copy)
);


-- This will initiate some of the logic
-- logic needs built to complete this request via forms  
INSERT INTO requests (user_id, space_number_id, building_number, access_approver_id, access_code_id, status_code)
VALUES (1, 'B24010101', 24, 1, 1, 1),
		(2, 'B24010101', 24, 1, 2, 1),
		(3, 'B24010101', 24, 1, 2, 1),
		(4, 'B24010101', 24, 1, 2, 1),
		(5, 'B24010101', 24, 1, 3, 1);


-- INSERT INTO key_inventory (transaction_id, key_number, key_copy, key_status_id)
-- VALUES (1, 43221, 1, 1),
-- 		(2, 56432, 1, 1),
-- 		(3, 59873, 3, 1),
-- 		(4, 34523, 1, 1),
-- 		(5, 46363, 2, 1);

--  determine if key is available in inventory




 
		
		

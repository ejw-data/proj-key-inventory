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
DROP TABLE IF EXISTS approvers CASCADE;
DROP TABLE IF EXISTS request_status;
DROP TABLE IF EXISTS approver_zones;
DROP TABLE IF EXISTS buildings CASCADE;
DROP TABLE IF EXISTS fabrication_status;
DROP TABLE IF EXISTS authentication;
DROP TABLE IF EXISTS order_status;

-- USERS ------------------------------------------------------
CREATE TABLE titles (
	title_id SERIAL PRIMARY KEY,
	title VARCHAR UNIQUE NOT NULL
);

CREATE TABLE roles (
	role_id SERIAL PRIMARY KEY,
	user_role VARCHAR UNIQUE NOT NULL
);

CREATE TABLE users (
	user_id SERIAL PRIMARY KEY,
	first_name VARCHAR NOT NULL,
	last_name VARCHAR NOT NULL,
	title_id INT REFERENCES titles (title_id),
	role_id INT REFERENCES roles (role_id),
	email VARCHAR UNIQUE NOT NULL,
	sponsor_id REFERENCES users (user_id)
);

-- make FK for role_approved_by - may need new table
CREATE TABLE approvers (
	approver_id SERIAL PRIMARY KEY,
	user_id INT REFERENCES users (user_id),
	role_approved_by INT NOT NULL,
	date_approved TIMESTAMP NOT NULL DEFAULT NOW(),
	date_removed TIMESTAMP
);

-- LOGIN _____________________________________________________

CREATE TABLE authentication (
	id INT PRIMARY KEY REFERENCES users (user_id),
	username VARCHAR UNIQUE NOT NULL,
	password_hash VARCHAR UNIQUE NOT NULL
);

-- SPACE & GRANTED APPROVAL ------------------------------------------------------------

CREATE TABLE buildings (
	building_number INT PRIMARY KEY,
	building_name VARCHAR UNIQUE NOT NULL,
	building_description VARCHAR NOT NULL
);

CREATE TABLE approver_zones (
	building_number INT REFERENCES buildings (building_number),
	approver_id INT REFERENCES approvers (approver_id),
	PRIMARY KEY (building_number, approver_id)
);

CREATE TABLE room_classification (
	room_type_id INT PRIMARY KEY,
	room_type VARCHAR UNIQUE NOT NULL
);

-- wing_number should be varchar; change name to wing_id
CREATE TABLE rooms (
	space_number_id VARCHAR PRIMARY KEY,
	building_number INT REFERENCES buildings (building_number),
	wing_number VARCHAR,  
	floor_number INT,
	room_number INT,
	room_type_id INT REFERENCES room_classification (room_type_id)
);

CREATE TABLE room_amenities (
	space_number_id VARCHAR PRIMARY KEY REFERENCES rooms (space_number_id),
	room_projector BOOL,
	room_seating INT
); 



-- ACCESS ASSIGNMENT -------------------------------------------------------------------
-- created_by and authorized_by should be references to Users and Approvers
CREATE TABLE access_codes (
	access_code_id SERIAL PRIMARY KEY,
	access_description VARCHAR,
	created_by INT,
	authorized_by INT,
	created_on TIMESTAMP NOT NULL DEFAULT NOW()
);

-- APPROVAL PROCESS ------------------------------------------------------------
CREATE TABLE request_status (
	request_status_id SERIAL PRIMARY KEY,
	request_status_name VARCHAR UNIQUE NOT NULL
);

-- logic updates status code
-- logic on update adds record to key_owner table the deletes record
CREATE TABLE requests (
	request_id SERIAL PRIMARY KEY,
	user_id INT,
	space_number_id VARCHAR,
	building_number INT,
	approver_id INT,
	access_code_id INT REFERENCES access_codes (access_code_id),
	request_status_id INT DEFAULT 1 REFERENCES request_status (request_status_id),
	request_date TIMESTAMP NOT NULL DEFAULT NOW(),
	approved_date TIMESTAMP,
	approved BOOL DEFAULT FALSE,
	approval_comment VARCHAR,
	rejection_comment VARCHAR,
	FOREIGN KEY (building_number, approver_id) REFERENCES approver_zones (building_number, approver_id)
);
-- ALTER TABLE requests ALTER COLUMN request_date SET DEFAULT now();
-- in the future move the comment to a separate table that includes the request_id/transaction_id


CREATE TABLE order_status (
	order_status_id SERIAL PRIMARY KEY,
	order_status VARCHAR UNIQUE NOT NULL
);

-- cannot make access_code_id a FK since it is not a primary key in requests table
-- instead of making a constraint, I will add this information via a trigger function
CREATE TABLE key_orders (
	request_id INT PRIMARY KEY REFERENCES requests (request_id),
	access_code_id INT REFERENCES access_codes (access_code_id),
	order_status_id INT REFERENCES order_status (order_status_id),
	date_key_received DATE,
	date_key_handoff DATE,
	key_admin_user_id INT,
	key_pickup_user_id INT,
	hold_on_conditions BOOL
);
-- maybe add a comments field or a separate table where all comments can be stored


CREATE TABLE access_pairs (
	access_code_id INT REFERENCES access_codes (access_code_id),
	space_number_id VARCHAR REFERENCES rooms (space_number_id),
	PRIMARY KEY (access_code_id, space_number_id) 
);
		
CREATE TABLE fabrication_status (
	fabrication_status_id SERIAL PRIMARY KEY,
	fabrication_status VARCHAR UNIQUE NOT NULL
);		

-- need to add constraint on key_maker_user_id
-- add logic to form that validates the key_copy number so duplicates are not possible
CREATE TABLE keys_created (
	request_id INT PRIMARY KEY,
	access_code_id INT REFERENCES access_codes (access_code_id),
	key_copy INT,
	fabrication_status_id INT DEFAULT 1 REFERENCES fabrication_status (fabrication_status_id),
	key_maker_user_id INT,
	date_created DATE
);

-- When copy and fabrication status are complete then it updates the inventory and triggers the key_order check  logic. 
-- The key_order needs a queue based on logic
-- Base the order on the transaction_id
CREATE TABLE key_status (
	key_status_id SERIAL PRIMARY KEY,
	key_status VARCHAR UNIQUE NOT NULL
);

-- need constraint that prevents duplicate key_acces_code_id and key_copy combinations
-- below will do this but there are no constrains on the keys_created table.
CREATE TABLE key_inventory (
	request_id INT PRIMARY KEY REFERENCES key_orders (request_id),
	access_code_id INT,
	key_copy INT,
	key_status_id INT REFERENCES key_status (key_status_id),
	date_transferred TIMESTAMP NOT NULL DEFAULT NOW(),
	date_returned TIMESTAMP,
	UNIQUE (access_code_id, key_copy)
);
-- Keys are first set by the keys_created in the key inventory table
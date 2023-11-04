DROP TABLE IF EXISTS key_junction;
DROP TABLE IF EXISTS keys;
DROP TABLE IF EXISTS access_pairs;
DROP TABLE IF EXISTS access_codes;
DROP TABLE IF EXISTS rooms;
DROP TABLE IF EXISTS room_amenities;
DROP TABLE IF EXISTS room_classification CASCADE;
DROP TABLE IF EXISTS key_owner;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS titles;
DROP TABLE IF EXISTS roles;
DROP TABLE IF EXISTS access_approvers;
DROP TABLE IF EXISTS access_zones;
DROP TABLES IF EXISTS buildings;



-- USERS ------------------------------------------------------
CREATE TABLE titles (
	title_id SERIAL PRIMARY KEY,
	title VARCHAR
);

INSERT INTO titles (title)
VALUES ('faculty'),
		('undergraduate student'),
		('graduate student'),
		('staff'),
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
		('admin')

CREATE TABLE users (
	user_id SERIAL PRIMARY KEY,
	first_name VARCHAR,
	last_name VARCHAR,
	title VARCHAR REFERENCES titles (title_id),
	user_role VARCHAR REFERENCES roles (user_role)
);

INSERT INTO users (first_name, last_name, title, user_role)
VALUES ('erin', 'wills', 1, 1),
		('will', 'wright', 1, 1),
		('andrew', 'ng', 1, 1),
		('bob', 'turtle', 5, 3),
		('jake', 'powers', 9, 3);
		

CREATE TABLE key_owner (
	owner_id INT PRIMARY KEY REFERENCES users (user_id)
);

INSERT INTO key_owner (owner_id)
VALUES (1),
		(2),
		(3);

CREATE TABLE access_approvers (
	access_approver_id SERIAL PRIMARY KEY,
	approver_id INT REFERENCES users (user_id),
	role_approved_by VARCHAR,
	date_approved TIMESTAMP NOT NULL DEFAULT NOW(),
	date_removed TIMESTAMP
);

INSERT INTO access_approvers (approver_id, role_approved_by)
VALUES (4, 9)

-- APPROVAL PROCESS ------------------------------------------------------------


CREATE TABLE approval_status (
	status_code SERIAL PRIMARY KEY,
	status_code_name VARCHAR
);

INSERT INTO approval_status (status_code_name)
VALUES ('REQUEST SUBMITTED'),
		('REQUEST APPROVED'),
		('KEY CREATED'),
		('KEY READY FOR PICKUP'),
		('KEY ISSUED');

-- requests table:  request_id, user_id, space, approver, status, dates, reasoning
-- logic updates record
-- logic on update adds record to key_owner table the deletes record
CREATE TABLE requests (
	request_id SERIAL PRIMARY KEY,
	user_id INT,
	space_number_id INT,
	access_approver_id INT,
	status_code INT REFERENCES approval_status (status_code),
	request_date TIMESTAMP NOT NULL DEFAULT NOW(),
	approved_date TIMESTAMP
);

-- Form updates to show only appropriate approvers
-- Submit Form
-- Approver gets dashboard updates based on query using status code
-- Approver approves and status changes
-- Key shop gets dashboard updates based on query using status code
-- Key shop makes key and enters key number and status updates and key/user_id updates
-- User picks up key and status updates

-- update requests status_code then update key_owner table then create key_junction entry 





-- SPACE & GRANTED APPROVAL ------------------------------------------------------------

CREATE TABLE buildings (
	bulding_number INT PRIMARY KEY,
	building_name VARCHAR,
	building_description VARCHAR
);

INSERT INTO buildings (building_number, building_name, building_description)
VALUES (24, 'Chemistry', 'Chemistry Department Research Space')


CREATE TABLE approver_zones (
	building_number PRIMARY KEY REFERENCES buildings (building_number),
	access_approver_id PRIMARY KEY REFERENCES access_approvers (access_approver_id)
);

INSERT INTO approver_zones (building_number, access_approver_id)
VALUES (24, 4)

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
	space_number_id INT PRIMARY KEY,
	building_number INT REFERENCES buildings (building_number),
	floor_number INT,
	wing_number INT,
	room_number INT,
	room_type INT REFERENCES room_classification (room_type_id)
);

INSERT INTO rooms (space_number, building_number, floor_number, wing_number, room_number, room_type, room_projector, room_seating)
VALUES ('24-01-01-01', 24, 01, 01, 01, 210),
		('24-02-01-01', 24, 02, 01, 01, 201),
		('24-02-01-02', 24, 02, 01, 02, 220);


CREATE TABLE room_amenities (
	space_number_id INT PRIMARY KEY REFERENCES rooms (space_number_id),
	room_projector BOOL,
	room_seating INT
); 

INSERT INTO room_amenities (space_number_id, room_projector, room_seating)
VALUES ('24-01-01-01', TRUE, 50),
		('24-02-01-01', FALSE, 1),
		('24-02-01-02', FALSE, 4);



-- ACCESS ASSIGNMENT -------------------------------------------------------------------

CREATE TABLE access_codes (
	access_code_id SERIAL PRIMARY KEY,
	access_description VARCHAR,
	created_by VARCHAR,
	authorized_by VARCHAR,
	created_on TIMESTAMP NOT NULL DEFAULT NOW()
);

INSERT INTO access_codes (access_code, access_description, created_by, authorized_by)
VALUES (1, 'Classroom', 'ejw', 'T. Bundy'),
		(2, 'Faculty Office and Suite', 'ejw', 'Prof. Andrews'),
		(3, 'Front Suite Only', 'ejw', 'Prof. Andrews');


CREATE TABLE access_pairs (
	access_code INT REFERENCES access_codes (access_code_id),
	space_number_id INT REFERENCES rooms (space_number_id),
	PRIMARY KEY (access_code_id, space_number_id) 
);

SELECT * FROM access_codes;

INSERT INTO access_pairs (access_code, room_number)
VALUES (1, 100),
		(2, 201),
		(2, 202),
		(3, 100),
		(3, 201),
		(3, 202);
		

CREATE TABLE keys (
	key_number INT PRIMARY KEY,
	key_copy INT,
	access_code INT REFERENCES access_codes (access_code)
);

INSERT INTO keys (key_number, key_copy, access_code)
VALUES (43221, 1, 3),
		(56432, 1, 1),
		(34523, 1, 2),
		(46363, 2, 2),
		(59873, 3, 2);


CREATE TABLE key_junction (
	owner_id INT REFERENCES key_owner (owner_id),
	key_number INT REFERENCES keys (key_number),
	PRIMARY KEY (owner_id, key_number)
);

INSERT INTO key_junction (owner_id, key_number)
VALUES (1, 43221),
		(4, 56432),
		(2, 59873),
		(3, 34523),
		(4, 46363);


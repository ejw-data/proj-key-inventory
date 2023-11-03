DROP TABLE IF EXISTS key_junction;
DROP TABLE IF EXISTS keys;
DROP TABLE IF EXISTS access_pairs;
DROP TABLE IF EXISTS access_codes;
DROP TABLE IF EXISTS rooms;
DROP TABLE IF EXISTS room_classification CASCADE;
DROP TABLE IF EXISTS key_owner;

-- Future work (to be added)
DROP TABLE IF EXISTS access_approvers;





CREATE TABLE key_owner (
	owner_id SERIAL PRIMARY KEY,
	owner_first_name VARCHAR,
	owner_last_name VARCHAR
);

CREATE TABLE access_approvers (
	access_approver_id SERIAL PRIMARY KEY,
	approver_id INT REFERENCES key_owner (owner_id),
	approved_by VARCHAR,
	date_approved TIMESTAMP NOT NULL DEFAULT NOW()
);

INSERT INTO key_owner (owner_first_name, owner_last_name)
VALUES ('erin', 'wills'),
		('will', 'wright'),
		('andrew', 'ng'),
		('bob', 'turtle');

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
	room_number INT PRIMARY KEY,
	room_type INT REFERENCES room_classification (room_type_id),
	room_projector BOOL,
	room_seating INT
);

INSERT INTO rooms (room_number, room_type, room_projector, room_seating)
VALUES (100, '210', TRUE, 50),
		(201, '201', FALSE, 1),
		(202, '220', FALSE, 4);
		
CREATE TABLE access_codes (
	access_code SERIAL PRIMARY KEY,
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
	access_code INT REFERENCES access_codes (access_code),
	room_number INT REFERENCES rooms (room_number),
	PRIMARY KEY (access_code, room_number) 
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


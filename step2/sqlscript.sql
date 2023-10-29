REM   Script: Lab2_step2
REM   Lab2 

CREATE TABLE galactic_race ( 
    race_id number NOT NULL UNIQUE, 
    race_name VARCHAR2(50) NOT NULL, 
    first_encounter_date DATE, 
    home_planet VARCHAR2(50) NOT NULL, 
    development_index NUMBER(4, 2), 
    CONSTRAINT race_name_pk PRIMARY KEY(race_name), 
    CONSTRAINT development_index_check CHECK (development_index >= 1 AND development_index <= 10) 
);

CREATE TABLE technology ( 
    technology_id number NOT NULL, 
    technology_name VARCHAR2(50), 
    invention_date DATE, 
    complexity_level NUMBER(10) NOT NULL, 
    application VARCHAR2(100), 
    race_name VARCHAR2(50) NOT NULL, 
    power_consumption NUMBER(5, 2), 
    CONSTRAINT technology_id_pk PRIMARY KEY (technology_id), 
    CONSTRAINT complexity_level_check CHECK (complexity_level >= 1 AND complexity_level <= 10), 
    CONSTRAINT race_name_fk FOREIGN KEY (race_name) REFERENCES galactic_race(race_name) 
);

INSERT INTO galactic_race VALUES (1, 'Time Lords', TO_DATE('1963-11-23', 'YYYY-MM-DD'), 'Gallifrey', 9.5);

INSERT INTO galactic_race VALUES (2, 'Humans', NULL, 'Earth', 3.6);

INSERT INTO galactic_race VALUES (3, 'Kaleds', NULL, 'Skaro', 6.1);

INSERT INTO galactic_race VALUES (4, 'Cyberman', TO_DATE('1903-1-1', 'YYYY-MM-DD'), 'Mondas', 5.2);

INSERT INTO galactic_race VALUES (5, 'Daleks', TO_DATE('1866-12-3', 'YYYY-MM-DD'), 'Skaro', 7.5);

select * from galactic_race;

INSERT INTO technology VALUES(1, 'TARDIS', NULL, 10, 'Time and Relative Dimension in Space',  (select race_name from galactic_race where race_id = 1), NULL);

INSERT INTO technology VALUES(2, 'Telephone', TO_DATE('1876-2-7', 'YYYY-MM-DD'), 5, 'Device for transmitting and receiving sound at a distance',  (select race_name from galactic_race where race_id = 2), 5);

INSERT INTO technology VALUES(3, 'Computer', TO_DATE('1939-5-29', 'YYYY-MM-DD'), 6, 'Data processing and information storage',  (select race_name from galactic_race where race_id = 2), 150);

INSERT INTO technology VALUES(4, 'Daleks', NULL, 9, 'Extermination and conquest', (select race_name from galactic_race where race_id = 3), NULL);

INSERT INTO technology VALUES(5, 'Temporal Vortex Manipulator', TO_DATE('5056-08-21', 'YYYY-MM-DD'), 8, 'Time travel and manipulation',  (select race_name from galactic_race where race_id = 1), 30.5);

INSERT INTO technology VALUES(6, 'Sonic Screwdriver', NULL, 7, 'Unlocking doors and manipulating technology',  (select race_name from galactic_race where race_id = 1), 5.5);

INSERT INTO technology VALUES(7, 'Temporal Ship of the Daleks', NULL, 10, 'Temporal manipulation and extermination', (select race_name from galactic_race where race_id = 5), NULL);

INSERT INTO technology VALUES(8, 'Cyber Ship', TO_DATE('1970-02-11', 'YYYY-MM-DD'), 9, 'Temporal invasion and extermination',(select race_name from galactic_race where race_id = 4), NULL);

INSERT INTO technology VALUES(9, 'Cyber Fleet Ship', TO_DATE('5100-5-26', 'YYYY-MM-DD'), 10, 'Temporal manipulation and conquest', (select race_name from galactic_race where race_id = 4), NULL);

INSERT INTO technology VALUES (10, 'Energy Blaster', NULL, 7, 'Cyberman extermination', (select race_name from galactic_race where race_id = 4), 10.55);

INSERT INTO technology VALUES (11, 'Temporal Regulator', TO_DATE('2025-03-15', 'YYYY-MM-DD'), 9, 'Time Travel', (select race_name from galactic_race where race_id = 5), 8.5);

INSERT INTO technology VALUES (12, 'Gravitational Cloud Generator', TO_DATE('2024-08-22', 'YYYY-MM-DD'), 6, 'Ship Concealmen', (select race_name from galactic_race where race_id = 5), 4.5);

select * from galactic_race;

select * from technology;


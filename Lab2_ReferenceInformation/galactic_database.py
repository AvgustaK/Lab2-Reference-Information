import sqlite3

# Подключение к базе данных (или ее создание, если не существует)
conn = sqlite3.connect('galactic_database.db')
print("Database created at:", conn)
cursor = conn.cursor()

# Создание таблицы galactic_race
cursor.execute('''
    CREATE TABLE IF NOT EXISTS galactic_race ( 
        race_id INTEGER PRIMARY KEY AUTOINCREMENT,
        race_name VARCHAR(50) NOT NULL UNIQUE, 
        first_encounter_date DATE, 
        home_planet VARCHAR(50) NOT NULL, 
        development_index NUMBER(4, 2),
        is_deleted INTEGER DEFAULT 0
    )
''')

# Создание таблицы technology
cursor.execute('''
    CREATE TABLE IF NOT EXISTS technology ( 
        technology_id INTEGER PRIMARY KEY AUTOINCREMENT,
        technology_name VARCHAR(50), 
        invention_date DATE, 
        complexity_level NUMBER(10) NOT NULL, 
        application VARCHAR(100), 
        race_name VARCHAR(50) NOT NULL, 
        power_consumption NUMBER(5, 2),
        is_deleted INTEGER DEFAULT 0,
        FOREIGN KEY (race_name) REFERENCES galactic_race(race_name)
    )
''')
# Вставка данных в таблицу galactic_race
cursor.executemany('''
    INSERT INTO galactic_race (race_name, first_encounter_date, home_planet, development_index)
    VALUES (?, ?, ?, ?)
''', [
    ('Time Lords', '1963-11-23', 'Gallifrey', 9.5),
    ('Humans', 'NULL', 'Earth', 3.6),
    ('Kaleds', 'NULL', 'Skaro', 6.1),
    ('Cyberman', '1903-1-1', 'Mondas', 5.2),
    ('Daleks', '1866-12-3', 'Skaro', 7.5),
])
# Вставка данных в таблицу technology
cursor.executemany('''
    INSERT INTO technology (technology_name, invention_date, complexity_level, application, race_name, power_consumption)
    VALUES (?, ?, ?, ?, ?, ?)
''', [
    ('TARDIS', 'NULL', 10, 'Time and Relative Dimension in Space', 'Time Lords', 'NULL'),
    ('Telephone', '1876-2-7', 5, 'Device for transmitting and receiving sound at a distance', 'Humans', 5),
    ('Computer', '1939-5-29', 6, 'Data processing and information storage', 'Humans', 150),
    ('Daleks', 'NULL', 9, 'Extermination and conquest', 'Kaleds', 'NULL'),
    ('Temporal Vortex Manipulator', '5056-08-21', 8, 'Time travel and manipulation', 'Time Lords', 30.5),
    ('Sonic Screwdriver', 'NULL', 7, 'Unlocking doors and manipulating technology', 'Time Lords', 5.5),
    ('Temporal Ship of the Daleks', 'NULL', 10, 'Temporal manipulation and extermination', 'Daleks', 'NULL'),
    ('Cyber Ship', '1970-02-11', 9, 'Temporal invasion and extermination', 'Cyberman', 'NULL'),
    ('Cyber Fleet Ship', '5100-5-26', 10, 'Temporal manipulation and conquest', 'Cyberman', 'NULL'),
    ('Energy Blaster', 'NULL', 7, 'Cyberman extermination', 'Cyberman', 10.55),
    ('Temporal Regulator', '2025-03-15', 9, 'Time Travel', 'Daleks', 8.5),
    ('Gravitational Cloud Generator', '2024-08-22', 6, 'Ship Concealmen', 'Daleks', 4.5),
])
# Сохранение изменений и закрытие соединения
conn.commit()
conn.close()
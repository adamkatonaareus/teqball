
import sqlite3 as sl
import config

con = sl.connect(config.DB_FOLDER + "teqball.db")

with con:
    con.execute("""
        CREATE TABLE HALL_OF_FAME (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            team TEXT,
            points INTEGER
        );
    """)


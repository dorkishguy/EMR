import sqlite3
from pathlib import Path
from datetime import date, datetime, timezone, timedelta

conn = sqlite3.connect("patients.db")
c = conn.cursor()

file_path = Path("patients.db")

def firstTime():
    c.execute("""
    CREATE TABLE IF NOT EXISTS patient_info (
    id INTEGER PRIMARY KEY,
    date TEXT,
    name TEXT,
    age INTEGER,
    sex INTEGER,
    bday TEXT,
    history TEXT
    );
    """)

firstTime()

def getInfo():
    datee = datetime.now(timezone(timedelta(hours=5, minutes=30))).isoformat().split("T")[0]
    name = input("Name: ")
    age = input("Age: ")
    sex = input("sex: ")
    while True:
        try:
            bday = input("Birth Date(YYYY-MM-DD): ")
            date.fromisoformat(bday)
            break
        except ValueError:
            print("Not a proper date")
    history = input("Patient history: ")
    return datee, name, age, sex, bday, history

def add_data(datee, name, age, sex, bday, history):
    c.execute(f"""
    INSERT INTO patient_info (date, name, age, sex, bday, history)
    VALUES ('{str(datee)}','{name}','{age}','{sex}','{bday}','{history}') 
    """)
    conn.commit()

def searchInfo():
    c.execute("SELECT * FROM patient_info")
    return c.fetchall()

def main():
    if not file_path.is_file():     
        firstTime()
    datee, name, age, sex, bday, history = getInfo()
    add_data(datee, name, age, sex, bday, history)
    searchInfo()
    conn.close()

if __name__ == "__main__":
    main()
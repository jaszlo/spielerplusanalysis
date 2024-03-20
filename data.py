from pathlib import Path
import pandas as pd
import duckdb
from tqdm import tqdm

from config import *
from EventType import EventType


class Database(object):
    def __init__(self):
        total_data = pd.DataFrame()
        self.name = "attendance.db"
        self.table =  "hunters_attendance"

        # Only read csv files if the database does not exist
        if Path("attendance.db").exists():
            return
        
        for path in tqdm(Path("./downloads").glob("*.csv"), desc="Reading CSVs"):
            df = pd.read_csv(path, sep=";", dtype="str")
            df["date"] = pd.to_datetime(df["event_date_start"], dayfirst=True)
            # Only keep the following columns
            df = df[["event_name","user_id", "user_name", "date"]]
            df = df.rename(columns={"event_name": "event_type"})
            total_data = pd.concat([total_data, df], axis=0)
    
    
        with duckdb.connect(self.name, read_only=False) as con:
            # Copy the dataframes into the database into a new table
            con.register("total_data", total_data)
            con.execute(f"CREATE OR REPLACE TABLE {self.table} AS SELECT * FROM total_data")

    
    def query_later_than(self, date):
        with duckdb.connect(self.name) as con:
            return con.query(f"SELECT * FROM {self.table} WHERE date > TIMESTAMP '{date}'").df()
        
    def query_ealier_than(self, date):
        with duckdb.connect(self.name) as con:
            return con.query(f"SELECT * FROM {self.table} WHERE date < TIMESTAMP '{date}'").df()

    def get_users(self):
        with duckdb.connect(self.name) as con:
            return con.query(f"SELECT DISTINCT user_name FROM {self.table}").df()["user_name"].tolist()

    def get_attendances(self, player_name, start_date=None, end_date=None, event_type=EventType.TRAINING):
        where_clause_player = f"WHERE user_name = '{player_name}'"
        where_clause_total = "WHERE 1=1"
        if start_date:
            where_clause_player += f" AND date > TIMESTAMP '{start_date}'"
            where_clause_total  += f" AND date > TIMESTAMP '{start_date}'"
        if end_date:
            where_clause_player += f" AND date < TIMESTAMP '{end_date}'"
            where_clause_total  += f" AND date < TIMESTAMP '{end_date}'"
        if event_type != EventType.ALL:
            where_clause_player += f" AND event_type = '{event_type}'"
            where_clause_total  += f" AND event_type = '{event_type}'"

        with duckdb.connect(self.name) as con:
            attended = len(con.query(f"SELECT DISTINCT date FROM {self.table} {where_clause_player}").df())
            total = len(con.query(f"SELECT DISTINCT date FROM {self.table} {where_clause_total}").df())

        return attended, total, attended / total if total > 0 else 0
        

    def get_attendances_for_season(self, year):
        start = f"{year}-08-01"
        end = f"{year + 1}-04-30"
        data = []
        for user_name in self.get_users():
            attendance = self.get_attendances(user_name, start, end, EventType.TRAINING)
            data.append((user_name, *attendance))
        
        # Sort by attendance
        data = sorted(data, key=lambda x: x[3], reverse=True)
        return data



if __name__ == "__main__":
    db = Database()
    for year in range(2017, 2024):
        data = db.get_attendances_for_season(year)
        print(f"Attendance for {year}/{year+1} ({data[0][2]} Trainings)")
        for place, (user_name, attended, total, percentage) in enumerate(data):
            space = 30 - len(user_name)
            print(f"#{place + 1}\t{user_name} {space * " "} attended {attended}\t ({percentage:.2%})")

        print("=" * 60)
        print("\n")  
    
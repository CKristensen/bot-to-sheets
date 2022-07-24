from dataclasses import dataclass
from datetime import date
from jobs.domain import Entry, AllergySymptoms, HealthStatus, FastingHours
from typing import List
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dateutil.parser import isoparse


class GoogleSheets:
    def __init__(self, key, creds):
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive.file",
            "https://www.googleapis.com/auth/drive",
        ]
        creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
        client = gspread.authorize(creds)
        self.sheet = client.open_by_key(key).sheet1

    def set(self, entry: Entry):
        self.sheet.append_row([entry.get_type(), entry.date.isoformat(), entry.level])

    def get_all(self) -> List[Entry]:
        data_list = self.sheet.get_all_records()  # Get a list of all records
        return_list = []
        print(data_list)
        for d in data_list:
            if d["entry_type"] == "allergy":
                return_list += [
                    AllergySymptoms(date=isoparse(d["date"]), level=d["content"])
                ]
            if d["entry_type"] == "health":
                return_list += [
                    HealthStatus(date=isoparse(d["date"]), level=d["content"])
                ]
            if d["entry_type"] == "fasting":
                return_list += [
                    FastingHours(date=isoparse(d["date"]), level=d["content"])
                ]
        return return_list


@dataclass
class FakeGoogleSheets(GoogleSheets):
    rows: List[Entry]

    def add(self, entry: Entry):
        self.rows += [entry]

    def get_all(self) -> List[Entry]:
        return self.rows

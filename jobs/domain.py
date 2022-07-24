from dataclasses import dataclass
from datetime import date


@dataclass
class Entry:
    date: date
    level: int

    def get_type(self) -> str:
        return "entry"

    @staticmethod
    def success_message(nentries):
        return "Success! Status Registered"

    @staticmethod
    def error_message():
        return "Failed! Invalid Status"


class AllergySymptoms(Entry):
    def get_type(self) -> str:
        return "allergy"

    @staticmethod
    def validate(status) -> bool:
        if status > 0:
            if status < 10:
                return True
        return False

    @staticmethod
    def success_message(nentries):
        return f"Success! Allergy symptoms Registered. Entries {nentries}"

    @staticmethod
    def error_message():
        return "Failed! Invalid allergy status"


class HealthStatus(Entry):
    def get_type(self) -> str:
        return "health"

    @staticmethod
    def validate(status) -> bool:
        if status > 0:
            if status < 10:
                return True
        return False

    @staticmethod
    def success_message(nentries):
        return f"Success! Health status registered. Number of entries {nentries}"

    @staticmethod
    def error_message():
        return "Failed! Invalid health status"


class FastingHours(Entry):
    def get_type(self) -> str:
        return "fasting"

    @staticmethod
    def validate(status) -> bool:
        if status > 0:
            return True
        else:
            return False

    @staticmethod
    def success_message(nentries):
        return f"Success! Fasting Hours registered. Number of entries {nentries}"

    @staticmethod
    def error_message():
        return "Failed! Invalid fasting hours"

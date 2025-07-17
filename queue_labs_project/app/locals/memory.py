import json
from pathlib import Path

ADMINS_FILE = Path(__file__).parent / "admins.json"

def load_admins() -> set[int]:
    try:
        with open(ADMINS_FILE, "r") as file:
            return set(json.load(file))
    except (FileNotFoundError, json.JSONDecodeError):
        return set()
            

def save_admins(admins: set[int]) -> None:
    with open(ADMINS_FILE, "w") as file:
        json.dump(list(admins), file)
    
    
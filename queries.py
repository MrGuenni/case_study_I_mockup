import json
from typing import List, Dict, Optional


class Database:
    def _init_(self, db_file: str):
        """
        Initialisiert die Database-Klasse, lädt Daten aus der JSON-Datei.
        :param db_file: Pfad zur JSON-Datenbankdatei
        """
        self.db_file = db_file
        self.data = self._load_data()

    def _load_data(self) -> Dict:
        """ Lädt die JSON-Datenbank aus der Datei. """
        try:
            with open(self.db_file, "r", encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            print("Error: Die Datenbankdatei wurde nicht gefunden.")
            return {}
        except json.JSONDecodeError:
            print("Error: Die Datenbankdatei ist nicht gültig.")
            return {}

    def get_all_devices(self) -> List[Dict]:
        """ Gibt alle Geräte aus der Datenbank zurück. """
        return self.data.get("devices", [])

    def find_device_by_name(self, name: str) -> Optional[Dict]:
        """
        Findet ein Gerät anhand des Namens.
        :param name: Der Name des gesuchten Geräts.
        :return: Das gefundene Gerät oder None, wenn es nicht existiert.
        """
        for device in self.data.get("devices", []):
            if device.get("device_name").lower() == name.lower():
                return device
        return None

    def get_devices_with_cost_above(self, cost: float) -> List[Dict]:
        """
        Filtert Geräte nach Wartungskosten.
        :param cost: Minimalwert der Wartungskosten.
        :return: Liste der Geräte, die die Kriterien erfüllen.
        """
        return [
            device
            for device in self.data.get("devices", [])
            if device.get("maintenance_cost", 0) > cost
        ]

    def add_device(self, new_device: Dict) -> bool:
        """
        Fügt ein neues Gerät zur Datenbank hinzu.
        :param new_device: Das Gerät als Dictionary.
        :return: True, wenn erfolgreich, False bei Fehlern.
        """
        if not isinstance(new_device, dict) or "device_id" not in new_device:
            print("Error: Ungültiges Gerätformat.")
            return False
        self.data.setdefault("devices", []).append(new_device)
        return self._save_data()

    def _save_data(self) -> bool:
        """ Speichert die aktuelle Datenbank in die JSON-Datei. """
        try:
            with open(self.db_file, "w", encoding="utf-8") as file:
                json.dump(self.data, file, indent=4, ensure_ascii=False)
            return True
        except IOError:
            print("Error: Fehler beim Speichern der Datenbank.")
            return False


# Beispielnutzung
if _name_ == "_main_":
    db = Database("database.json")

    # Alle Geräte ausgeben
    print("Alle Geräte in der Datenbank:")
    for device in db.get_all_devices():
        print(device)

    # Gerät nach Name suchen
    search_name = "Laptop"
    result = db.find_device_by_name(search_name)
    if result:
        print(f"\nGerät '{search_name}' gefunden:")
        print(result)
    else:
        print(f"\nGerät '{search_name}' nicht gefunden.")

    # Geräte nach Wartungskosten filtern
    min_cost = 10.0
    print(f"\nGeräte mit Wartungskosten über {min_cost}:")
    filtered_devices = db.get_devices_with_cost_above(min_cost)
    for device in filtered_devices:
        print(device)

    # Ein neues Gerät hinzufügen
    new_device = {
        "device_id": 4,
        "device_name": "Smartphone",
        "device_type": "Typ D",
        "device_description": "Diensthandy für Techniker",
        "responsible_person": {
            "user_id": "user2",
            "username": "Andre",
            "email": "andre@example.com",
            "role": "Techniker"
        },
        "end_of_life": "2026-12-31",
        "maintenance_cost": 20.0
    }
    if db.add_device(new_device):
        print("\nNeues Gerät wurde hinzugefügt!")
    else:
        print("\nFehler beim Hinzufügen des neuen Geräts.")
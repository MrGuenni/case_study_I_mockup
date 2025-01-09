import streamlit as st
from backend import UserDatabase, ReservationDatabase, DeviceDatabase
from tinydb import Query

def create_new_user():
    st.title("Nutzer anlegen")
    username = st.text_input("Benutzername")
    email = st.text_input("E-Mail")
    role = st.selectbox("Rolle", ["Geräteverantwortlicher", "Reservierer"])
    submitted = st.button("Nutzer anlegen")
    if submitted:
        user_db = UserDatabase()
        result = user_db.add_user(username, email, role)
        if result:
            st.success("Nutzer erfolgreich angelegt.")
        else:
            st.error("Fehler beim Anlegen des Nutzers.")

def create_or_remove_reservation():
    st.title("Reservierung anlegen oder entfernen")
    devices_db = DeviceDatabase()
    users_db = UserDatabase()
    reservations_db = ReservationDatabase()

    # Auswahlboxen für Geräte und Nutzer
    devices = devices_db.get_all_devices()
    users = users_db.get_all_users()

    if not devices or not users:
        st.warning("Keine Geräte oder Nutzer vorhanden.")
        return

    device_options = {device['device_id']: device for device in devices}
    user_options = {user['user_id']: user for user in users}

    selected_device_id = st.selectbox("Gerät auswählen", list(device_options.keys()), format_func=lambda x: device_options[x]['device_name'])
    selected_user_id = st.selectbox("Nutzer auswählen", list(user_options.keys()), format_func=lambda x: user_options[x]['username'])

    start_date = st.date_input("Startdatum")
    end_date = st.date_input("Enddatum")

    if st.button("Reservierung anlegen"):
        result = reservations_db.add_reservation(selected_device_id, selected_user_id, start_date, end_date)
        if result:
            st.success("Reservierung erfolgreich angelegt.")
        else:
            st.error("Fehler bei der Reservierung.")

    if st.button("Reservierung entfernen"):
        result = reservations_db.remove_reservation(selected_device_id, selected_user_id, start_date, end_date)
        if result:
            st.success("Reservierung erfolgreich entfernt.")
        else:
            st.error("Fehler beim Entfernen der Reservierung.")

    st.subheader("Aktuelle Reservierungen")
    current_reservations = reservations_db.get_current_reservations_with_details()
    if current_reservations:
        for res in current_reservations:
            st.write(f"Gerät: {res['device_name']}, Nutzer: {res['user_name']}, Zeitraum: {res['start_date']} bis {res['end_date']}")
    else:
        st.info("Keine aktuellen Reservierungen vorhanden.")

from flask import Flask, request, jsonify
import pandas as pd
import os
import json
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

# File paths
USERS_FILE = "users.csv"
USER_EVENTS_FILE = "user_events.csv"

# Initialize users.csv with headers if it doesn't exist
if not os.path.exists(USERS_FILE):
    df = pd.DataFrame(columns=["name", "email", "phone", "uniqueId", "registered_events"])
    df.to_csv(USERS_FILE, index=False)

# Initialize user_events.csv with default events if it doesn't exist
if not os.path.exists(USER_EVENTS_FILE):
    default_events = [
        {"name": "Tech Summit 2025", "location": "New York", "date": "2025-06-15", "time": "", "type": "Conference", "description": "A summit for tech enthusiasts.", "bannerUrl": "", "hostEmail": "default@gmail.com"},
        {"name": "Music Fest 2025", "location": "Berlin", "date": "2025-07-20", "time": "", "type": "Concert", "description": "An annual music festival.", "bannerUrl": "", "hostEmail": "default@gmail.com"},
        {"name": "AI Workshop", "location": "Tokyo", "date": "2025-08-10", "time": "", "type": "Workshop", "description": "Learn about AI advancements.", "bannerUrl": "", "hostEmail": "default@gmail.com"},
        {"name": "Cyber Expo 2025", "location": "London", "date": "2025-09-05", "time": "", "type": "Exhibition", "description": "Explore the latest in cybersecurity.", "bannerUrl": "", "hostEmail": "default@gmail.com"},
        {"name": "Future Tech Hackathon", "location": "San Francisco", "date": "2025-10-12", "time": "", "type": "Hackathon", "description": "Innovate and build future tech solutions.", "bannerUrl": "", "hostEmail": "default@gmail.com"},
        {"name": "Neon Dance Party", "location": "Miami", "date": "2025-11-20", "time": "", "type": "Party", "description": "A vibrant dance party with neon lights.", "bannerUrl": "", "hostEmail": "default@gmail.com"},
        {"name": "Space Exploration Seminar", "location": "Houston", "date": "2025-12-01", "time": "", "type": "Seminar", "description": "Dive into the future of space travel.", "bannerUrl": "", "hostEmail": "default@gmail.com"},
        {"name": "Virtual Reality Summit", "location": "Seoul", "date": "2025-12-15", "time": "", "type": "Conference", "description": "Experience the latest in VR technology.", "bannerUrl": "", "hostEmail": "default@gmail.com"}
    ]
    df = pd.DataFrame(default_events)
    df.to_csv(USER_EVENTS_FILE, index=False)

# Ensure users.csv has the registered_events column
users_df = pd.read_csv(USERS_FILE)
if "registered_events" not in users_df.columns:
    users_df["registered_events"] = users_df.apply(lambda _: "[]", axis=1)
    users_df.to_csv(USERS_FILE, index=False)

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')
    uniqueId = data.get('uniqueId')

    if not all([name, email, phone, uniqueId]):
        return jsonify({"error": "Missing required fields"}), 400

    users_df = pd.read_csv(USERS_FILE)
    if email in users_df['email'].values:
        return jsonify({"error": "Email already registered"}), 400

    new_user = pd.DataFrame({
        "name": [name],
        "email": [email],
        "phone": [phone],
        "uniqueId": [uniqueId],
        "registered_events": ["[]"]
    })
    users_df = pd.concat([users_df, new_user], ignore_index=True)
    users_df.to_csv(USERS_FILE, index=False)
    return jsonify({"message": "Signup successful"}), 200

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    uniqueId = data.get('uniqueId')

    if not all([email, uniqueId]):
        return jsonify({"error": "Missing required fields"}), 400

    users_df = pd.read_csv(USERS_FILE)
    user = users_df[(users_df['email'] == email) & (users_df['uniqueId'] == uniqueId)]
    if user.empty:
        return jsonify({"error": "Invalid email or unique ID"}), 401

    user_data = user.iloc[0].to_dict()
    return jsonify({
        "message": "Login successful",
        "user": {
            "name": user_data['name'],
            "email": user_data['email'],
            "uniqueId": user_data['uniqueId'],
            "registered_events": json.loads(user_data['registered_events'])
        }
    }), 200

@app.route('/host_event', methods=['POST'])
def host_event():
    data = request.get_json()
    name = data.get('name')
    date = data.get('date')
    time = data.get('time')
    location = data.get('location')
    description = data.get('description', '')
    bannerUrl = data.get('bannerUrl', '')
    hostEmail = data.get('hostEmail')

    required_fields = [name, date, time, location, hostEmail]
    if not all(required_fields) or any(field.strip() == '' for field in required_fields if isinstance(field, str)):
        return jsonify({"error": "Missing or empty required fields"}), 400

    try:
        event_date = datetime.strptime(date, '%Y-%m-%d')
        today = datetime.strptime('2025-05-13', '%Y-%m-%d')
        if event_date < today:
            return jsonify({"error": "Event date cannot be in the past"}), 400
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400

    try:
        user_events_df = pd.read_csv(USER_EVENTS_FILE)
        new_event = pd.DataFrame({
            "name": [name],
            "date": [date],
            "time": [time],
            "location": [location],
            "description": [description],
            "bannerUrl": [bannerUrl],
            "hostEmail": [hostEmail],
            "type": ['']
        })
        user_events_df = pd.concat([user_events_df, new_event], ignore_index=True)
        user_events_df.to_csv(USER_EVENTS_FILE, index=False)
    except Exception as e:
        return jsonify({"error": f"Failed to save event: {str(e)}"}), 500

    return jsonify({"message": "Event hosted successfully"}), 200

@app.route('/get_events', methods=['GET'])
def get_events():
    location = request.args.get('location', '')
    date = request.args.get('date', '')
    event_type = request.args.get('type', '')

    try:
        events_df = pd.read_csv(USER_EVENTS_FILE) if os.path.exists(USER_EVENTS_FILE) else pd.DataFrame(columns=["name", "date", "time", "location", "description", "bannerUrl", "hostEmail", "type"])
        
        expected_columns = ["name", "date", "time", "location", "description", "bannerUrl", "hostEmail", "type"]
        for col in expected_columns:
            if col not in events_df.columns:
                events_df[col] = ''
        
        events_df = events_df.fillna('')

        if location:
            events_df = events_df[events_df['location'] == location]
        if date:
            events_df = events_df[events_df['date'] == date]
        if event_type:
            events_df = events_df[events_df['type'] == event_type]

        events = events_df.to_dict('records')
        return jsonify(events), 200

    except Exception as e:
        print(f"Error in get_events: {str(e)}")
        return jsonify({"error": f"Failed to fetch events: {str(e)}"}), 500

@app.route('/register_event', methods=['POST'])
def register_event():
    data = request.get_json()
    email = data.get('email')
    event_name = data.get('event_name')
    lunch_preference = data.get('lunch_preference', {})

    if not all([email, event_name]):
        return jsonify({"error": "Missing required fields"}), 400

    users_df = pd.read_csv(USERS_FILE)
    user_index = users_df.index[users_df['email'] == email]
    if user_index.empty:
        return jsonify({"error": "User not found"}), 404

    user = users_df.loc[user_index[0]]
    registered_events = json.loads(user['registered_events'])

    # Convert old formats to the new format
    if isinstance(registered_events, list) and all(isinstance(event, str) for event in registered_events):
        # Old format: list of strings
        registered_events = [{"event_name": event_name, "lunch_preference": {"main_preference": "", "additional_info": ""}} for event_name in registered_events]
    elif isinstance(registered_events, list) and all(isinstance(event, dict) and isinstance(event.get('lunch_preference'), str) for event in registered_events):
        # Previous format: lunch_preference as a string
        registered_events = [{"event_name": event['event_name'], "lunch_preference": {"main_preference": event['lunch_preference'], "additional_info": ""}} for event in registered_events]
    elif not isinstance(registered_events, list):
        registered_events = []

    # Check if the event is already registered
    if any(event['event_name'] == event_name for event in registered_events):
        return jsonify({"error": "Event already registered"}), 400

    # Add the event with lunch preference
    registered_events.append({
        "event_name": event_name,
        "lunch_preference": {
            "main_preference": lunch_preference.get('main_preference', ''),
            "additional_info": lunch_preference.get('additional_info', '')
        }
    })
    users_df.at[user_index[0], 'registered_events'] = json.dumps(registered_events)
    users_df.to_csv(USERS_FILE, index=False)
    return jsonify({"message": f"Successfully registered for {event_name}"}), 200

@app.route('/remove_event', methods=['POST'])
def remove_event():
    data = request.get_json()
    email = data.get('email')
    event_name = data.get('event_name')

    if not all([email, event_name]):
        return jsonify({"error": "Missing required fields"}), 400

    users_df = pd.read_csv(USERS_FILE)
    user_index = users_df.index[users_df['email'] == email]
    if user_index.empty:
        return jsonify({"error": "User not found"}), 404

    user = users_df.loc[user_index[0]]
    registered_events = json.loads(user['registered_events'])
    
    # Handle all possible formats
    if isinstance(registered_events, list) and all(isinstance(event, str) for event in registered_events):
        if event_name not in registered_events:
            return jsonify({"error": "Event not found in registered events"}), 404
        registered_events.remove(event_name)
    else:
        # New format: list of objects
        registered_events = [event for event in registered_events if event['event_name'] != event_name]

    users_df.at[user_index[0], 'registered_events'] = json.dumps(registered_events)
    users_df.to_csv(USERS_FILE, index=False)
    return jsonify({"message": f"Successfully removed {event_name} from registered events"}), 200

@app.route('/user_events', methods=['GET'])
def get_user_events():
    email = request.args.get('email')
    if not email:
        return jsonify({"error": "Email is required"}), 400

    users_df = pd.read_csv(USERS_FILE)
    user = users_df[users_df['email'] == email]
    if user.empty:
        return jsonify({"error": "User not found"}), 404

    registered_events = json.loads(user.iloc[0]['registered_events'])
    # Handle all formats
    if isinstance(registered_events, list) and all(isinstance(event, str) for event in registered_events):
        event_names = registered_events
    else:
        event_names = [event['event_name'] for event in registered_events]
    return jsonify({"registered_events": event_names}), 200

@app.route('/get_hosted_events', methods=['GET'])
def get_hosted_events():
    email = request.args.get('email')
    if not email:
        return jsonify({"error": "Email is required"}), 400

    try:
        events_df = pd.read_csv(USER_EVENTS_FILE) if os.path.exists(USER_EVENTS_FILE) else pd.DataFrame(columns=["name", "date", "time", "location", "description", "bannerUrl", "hostEmail", "type"])
        
        expected_columns = ["name", "date", "time", "location", "description", "bannerUrl", "hostEmail", "type"]
        for col in expected_columns:
            if col not in events_df.columns:
                events_df[col] = ''
        
        events_df = events_df.fillna('')

        hosted_events = events_df[events_df['hostEmail'] == email]
        events = hosted_events.to_dict('records')
        return jsonify(events), 200

    except Exception as e:
        print(f"Error in get_hosted_events: {str(e)}")
        return jsonify({"error": f"Failed to fetch hosted events: {str(e)}"}), 500

@app.route('/get_event_registrations', methods=['GET'])
def get_event_registrations():
    event_name = request.args.get('event_name')
    if not event_name:
        return jsonify({"error": "Event name is required"}), 400

    try:
        users_df = pd.read_csv(USERS_FILE)
        registered_users = []

        for index, user in users_df.iterrows():
            registered_events = json.loads(user['registered_events'])
            lunch_preference = {"main_preference": "", "additional_info": ""}
            
            # Handle all possible formats of registered_events
            if isinstance(registered_events, list) and all(isinstance(event, str) for event in registered_events):
                if event_name in registered_events:
                    registered_users.append({
                        "name": user['name'],
                        "email": user['email'],
                        "phone": user['phone'],
                        "lunch_preference": lunch_preference
                    })
            elif isinstance(registered_events, list) and all(isinstance(event, dict) and isinstance(event.get('lunch_preference'), str) for event in registered_events):
                # Previous format: lunch_preference as a string
                event_entry = next((event for event in registered_events if event['event_name'] == event_name), None)
                if event_entry:
                    lunch_preference = {"main_preference": event_entry['lunch_preference'], "additional_info": ""}
                    registered_users.append({
                        "name": user['name'],
                        "email": user['email'],
                        "phone": user['phone'],
                        "lunch_preference": lunch_preference
                    })
            else:
                # Current format: lunch_preference as an object
                event_entry = next((event for event in registered_events if event['event_name'] == event_name), None)
                if event_entry:
                    lunch_preference = event_entry.get('lunch_preference', {"main_preference": "", "additional_info": ""})
                    registered_users.append({
                        "name": user['name'],
                        "email": user['email'],
                        "phone": user['phone'],
                        "lunch_preference": lunch_preference
                    })

        return jsonify(registered_users), 200

    except Exception as e:
        print(f"Error in get_event_registrations: {str(e)}")
        return jsonify({"error": f"Failed to fetch event registrations: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
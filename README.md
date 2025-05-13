# Snuccc-Inductions-Prithvirajrp

ok so hi guys , this is prithviraj rp , first year AIDS B ;)

(my favourite flavour of icecream is pista btw)

To test out this project login with the email as a@gmail.com and password as "vanilla-11223333" ( its one of the user login profile where i have hosted an event. )


Skibidi Event Manager

# Prerequisites
Before running the project, ensure you have the following installed:

Python 3.8+: For running the Flask backend server.
pip: To install Python dependencies.
Node.js (optional): Only if you need to serve the frontend independently.
A modern web browser: Chrome, Firefox, or Edge recommended.

# Installation

Clone the Repository:
git clone https://github.com/your-username/skibidi-event-manager.git
cd skibidi-event-manager


# Set Up the Backend:

Install the required Python packages:pip install flask pandas


Ensure app.py (the Flask server) is in the project root.



# Prepare the Frontend:

The frontend consists of HTML files (index.html, home.html, host_dashboard.html, etc.).
No additional setup is required as it uses CDN-hosted libraries (Tailwind CSS, Chart.js).


# Start the Backend Server:

Run the Flask server to handle API requests:python app.py


The server will start on http://localhost:5000.


# Serve the Frontend:

Use a local server to serve the HTML files:python -m http.server 8000


Access the app at http://localhost:8000.

# Overview
Skibidi Event Manager is a web-based application designed to streamline event hosting and participation. It allows users to create, manage, and register for events, with features tailored for both event hosts and attendees. The app features a futuristic dark-themed interface with interactive elements, making event management both efficient and engaging.
This project was developed as a submission for a judging panel, showcasing our skills in web development, data visualization, and user experience design.
Features

Event Hosting: Create and manage events with details like name, date, location, type, and description.
Event Registration: Users can browse and register for events, specifying lunch preferences (Vegan/Non-Vegan).
Host Dashboard: Provides hosts with:
Quick stats (total events, registrations, most popular event).
A pie chart for lunch preference distribution (using Chart.js).
Option to export registration data as a CSV file.


Registered Events Page: Attendees can view and manage their registered events.
Responsive Design: Works seamlessly across devices with a grid-based layout for event cards.
Interactive UI: Features a dark gradient theme, Orbitron font, glowing hover effects, and slide-in notifications.





# Usage

Access the App:

Open http://localhost:8000/index.html in your browser to start.
Log in or sign up to access the app's features.


As an Attendee:

Navigate to home.html to view available events.
Register for an event by providing your details and lunch preference.
Go to registered_events.html to see your registered events and remove registrations if needed.


As a Host:

Go to host_event.html to create a new event.
Visit host_dashboard.html to:
View quick stats (total events, registrations, etc.).
See your hosted events and their registrations.
Use the pie chart to visualize lunch preferences.
Export registration data as a CSV file.



Technologies Used

Frontend:
HTML, JavaScript
Tailwind CSS (via CDN) for styling
Chart.js (via CDN) for data visualization
Orbitron font for a futuristic look


Backend:
Flask (Python) for API endpoints
Pandas for handling CSV data


Storage:
Local storage for user sessions
CSV files for persistent data



Future Improvements

Add real-time event updates using WebSockets.
Implement user profiles with avatars and event history.
Integrate a payment system for paid events.
Enhance accessibility with ARIA labels and keyboard navigation.
Deploy the app on a cloud platform for broader access.

Contact:

Email: r.p.prithviraj2007@gmail.com
GitHub Issues: Feel free to open an issue on this repository for bugs or suggestions.





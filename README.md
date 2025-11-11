# self_service
A simple, lightweight REST API built with Flask, Netmiko, and ping3 to provide "self-service" network automation tasks.


Self-Service Network API (Flask)

A simple, lightweight REST API built with Flask, Netmiko, and ping3 to provide "self-service" network automation tasks.

Instead of running manual CLI commands, this app provides simple web endpoints to run network diagnostics and pull data, with the results returned as JSON. This project is a proof-of-concept for building scalable, event-driven network automation tools.

Features

/: A simple health-check endpoint.

/api/ping/<ip_address>: Runs a live ping test against any IP and returns the status and round-trip time.

/api/ssh/<device_name>/<command_str>: Connects to a pre-defined device (from a local "source of truth") and runs any read-only show command.

Tech Stack

Python 3

Flask: The web server framework.

Netmiko: For SSH connectivity and command execution.

ping3: A simple, cross-platform Python ping library.

Setup & Installation

Follow these steps to get the app running locally.

1. Clone the Repository

git clone https://github.com/YourUsername/your-repo-name.git
cd your-repo-name


2. Create a Virtual Environment (Best Practice)

This isolates your project's dependencies from your system.

# Create the virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate


3. Install Dependencies

Install all required libraries from the requirements.txt file.

pip install -r requirements.txt


4. Configure Devices

This app uses a simple Python dictionary in app.py as its "Source of Truth." You must edit the DEVICES constant with your own lab device information.

# app.py
...
DEVICES = {
    "R1": {
        "host": "10.0.0.78",
        "device_type": "cisco_ios",
        "username": "YOUR_USERNAME",  # <-- CHANGE THIS
        "password": "YOUR_PASSWORD"   # <-- CHANGE THIS
    },
    "R2": {
        # ...
    }
}
...


5. Run the App

python3 app.py


The server will start on http://127.0.0.1:5000 (or 5001 if you changed the port).

Usage (API Endpoints)

You can use curl or your web browser to test the endpoints.

Health Check

Endpoint: GET /

curl Command:

curl http://127.0.0.1:5000/


Success Response:

{
  "message": "Hello, World! Your API is running."
}


Ping an IP

Endpoint: GET /api/ping/<ip_address>

curl Command:

curl http://127.0.0.1:5000/api/ping/10.0.0.78


Success Response:

{
  "ip": "10.0.0.78",
  "rtt_ms": 1.25,
  "status": "ok"
}


Failure Response:

{
  "ip": "1.1.1.1",
  "message": "Host is DOWN",
  "status": "error"
}


Run an SSH Command

Endpoint: GET /api/ssh/<device_name>/<command_str>

Note: The app replaces _ (underscores) in the URL with spaces for the command.

curl Command:

# To run "show ip interface brief"
curl http://127.0.0.1:5000/api/ssh/R1/show_ip_interface_brief


Success Response:

{
  "command": "show ip interface brief",
  "device": "R1",
  "output": "Interface              IP-Address      OK? Method Status                Protocol\nGigabitEthernet0/0     10.0.0.78       YES NVRAM  up                    up      \nLoopback99             1.1.1.1         YES manual up                    up      ",
  "status": "success"
}

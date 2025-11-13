
Self-Service Network API (Flask)

A simple "self-service" API built with Flask and Netmiko. Its job is to provide simple, pre-defined "show" commands and ping tests to other users without giving them direct SSH access.

This project was built to practice "production-ready" Python, including API development (Flask), secure config management, and automation logic (Netmiko).

Tech Stack

Flask: The web server framework.

Netmiko: For SSH connectivity and command execution.

Loguru: For "production-ready" logging.

PyYAML: For parsing the external configuration file.

ping3: A simple, cross-platform Python ping library.

Setup & Installation

Follow these "production-ready" steps to get the app running locally.

1. Clone the Repository

git clone [YOUR_REPO_URL]
cd [YOUR_REPO_NAME]


2. Create a Virtual Environment (Best Practice)

This isolates your project's dependencies from your system.

# Create the virtual environment
python3 -m venv venv

# Activate it (for Mac/Linux)
source venv/bin/activate


3. Install Dependencies

Install all required libraries from the requirements.txt file.

# This will install Flask, Netmiko, Loguru, PyYAML, etc.
pip install -r requirements.txt


4. Create Your "Source of Truth" (inventory.yml)

This app loads all device info (including secrets) from inventory.yml. This file MUST NOT be committed to Git.

Create the file:
nano inventory.yml

Paste this template and add your device info:

# This is your external Source of Truth
devices:
  R1:
    host: "10.0.0.78"
    device_type: "cisco_ios"
    username: "your_lab_username"
    password: "your_lab_password"
  R2:
    host: "10.0.0.79"
    device_type: "cisco_ios"
    username: "your_lab_username"
    password: "your_lab_password"


5. CRITICAL: Secure Your Secrets

You just put secrets in inventory.yml. You must tell Git to ignore this file.

Create/edit your .gitignore file:
nano .gitignore

Add this line:

inventory.yml


Running the App

1. Set Environment Variables

This app uses os.environ to identify the developer.

# For Mac/Linux
export DEVELOPER="Jeff"


2. Run the App

CRITICAL: Because of how the CONFIG_FILE path is built, you must run this app from the root of the project directory.

# From your project's root folder:
python3 app.py


The server will start on http://127.0.0.1:5000.

Usage (API Endpoints)

You can use curl or your web browser to test the endpoints.

Health Check

Endpoint: GET /

curl Command:

curl [http://127.0.0.1:5000/](http://127.0.0.1:5000/)


Success Response (from your code):

{
  "MESSAGE": "Nice, the API is running!. "
}


Ping an IP

Endpoint: GET /api/ping/<ip_address>

curl Command:

curl [http://127.0.0.1:5000/api/ping/10.0.0.78](http://127.0.0.1:5000/api/ping/10.0.0.78)


Success Response:

{
  "ip": "10.0.0.78",
  "rtt_ms": 1.25,
  "status": "ok"
}


Failure Response (from your code):

{
  "ip": "1.1.1.1",
  "message": "OH NO! THE HOST IS DOWN",
  "status": "error"
}


Run an SSH Command

Endpoint: GET /api/ssh/<device_name>/<command_str>

Note: The app replaces _ (underscores) in the URL with spaces for the command.

curl Command:

# To run "show ip interface brief"
curl [http://127.0.0.1:5000/api/ssh/R1/show_ip_interface_brief](http://127.0.0.1:5000/api/ssh/R1/show_ip_interface_brief)


Success Response:

{
  "command": "show ip interface brief",
  "device": "R1",
  "output": "Interface              IP-Address      OK? Method Status ...",
  "status": "success"
}


Failure Response (from your code):

{
  "message": "Sorry man...Device 'R3' not found.",
  "status": "error"
}

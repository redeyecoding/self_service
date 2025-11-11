from flask import Flask, jsonify
import ping3
from netmiko import ConnectHandler
import os

DEFAULT_USERNAME = os.environ["DEFAULT_USERNAME"]
DEFAULT_PASSWORD = os.environ["DEFAULT_PASSWORD"]
DEVELOPER = os.environ["DEVELOPER"]

# PUT THIS IN A DATABASE FILE FOR PRODUCTION NETWORKS
DEVICES = {
    "newyork_rtr_1": {
        "host": "10.0.0.78",
        "device_type": "cisco_ios",
        "username": DEFAULT_USERNAME,
        "password": DEFAULT_PASSWORD
    }

}

#LETS RUN A SINGLE COMMAND PLEASE :0)
def run_ssh_command(device, command):
    '''
        My helper function to connect and run a single command to the CPE
    '''
    try:

        device_name = device.pop("device_name", None)

        with ConnectHandler(**device) as net_connect:
            cpe_output = net_connect.send_command(command)

        device["device_name"] = device_name
        return {
            "status": "success",
            "device": device_name,
            "command": command,
            "output": cpe_output
        }
    
    except Exception as oops_error:
        return {
            "status": "ERROR!",
            "device": device.get("device_name","unknown"),
            "command": command,
            "cpe_error_message": str(oops_error)
        }


# FLASK

app = Flask(__name__)

@app.route("/")
def confirm_running_api():
    '''
        JUST TESTING TO MAKE SURE THE API IS RUNNING
    '''
    return jsonify({"MESSAGE": f"{DEVELOPER}'s API is running!. "})

@app.route("/api/ping/<ip_address>")
def ping_ip(ip_address):
    '''
        runs a standard ping test against the target ip address
    '''
    print(f" **---- Recived ping request for: {ip_address} ----** ")
    redeye_rtt = ping3.ping(ip_address, timeout=1)

    if redeye_rtt is None:
        return jsonify({"status": "error", "ip": ip_address, "message": "OH NO! THE HOST IS DOWN"}), 404
    else:
        return jsonify({"status": "ok", "ip": ip_address, "rtt_ms": round(redeye_rtt * 1000, 2)})
    

@app.route("/api/ssh/<device_name>/<command_str>")
def run_ssh(device_name, command_str):
    '''
        All this does is Connects to a pre-defined device and runs a show command.
    '''
    print(f" --- Received SSH request for: {device_name} ---")

    #search for the device in 'DEVICESS' constant
    if device_name not in DEVICES:
        return jsonify({"status": "error", "message": f"Sorry man...Device '{device_name}' not found."}), 404
    
    #DO NOT MODIFY - this grabs a copy of the device info so we don't mess up the original
    device_info = DEVICES[device_name].copy()
    device_info["device_name"] = device_name # primary use for the helper function.

    #get rid of the underScores
    command = command_str.replace("_", " ")

    result = run_ssh_command(device_info, command)

    if result["status"] == "error":
        return jsonify(result), 500
    else:
        return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

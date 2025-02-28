import obd
import argparse
import time
import datetime

parser = argparse.ArgumentParser()
parser.add_argument('--command', '-c', type=str, help='the command to execute', required=True)
parser.add_argument('--port', '-p', type=str, help='The OBD-II connection port (e.g., /dev/ttyUSB0 or COM3)', required=True)
parser.add_argument('--listen', '-l', action='store_true', help='If command "GET_DTC" it will listen for dtc errors', required=False)
args = parser.parse_args()

command = args.command.lower().strip()
port = args.port.lower().strip()
listen = args.listen

print(f"{listen =}")
print(f"{command =}")
print(f"{port =}")  

if args.listen and not command == 'get_dtc':
    raise Exception("Listen only works with command 'get_dtc'")

def query(connection, cmd):
    def write_to_file(response):
        if response.value is not None:
            value_to_log = str(response.value)
        else:
            value_to_log = "No value returned"
        print(value_to_log)
        try:
            with open("dtc_logs", "a") as f:
                f.write(f"\nLog created on {datetime.datetime.now()}\n")
                f.write(f"{response.value} \n")
        except Exception as e:
            print(f"Failed to write to log file {str(e)}")
            
    response = connection.query(cmd)
    write_to_file(response=response)
    return response

connection = obd.OBD(port)

command_map = {
    "rpm": obd.commands.RPM,
    "speed": obd.commands.SPEED,
    "throttle": obd.commands.THROTTLE_POS,
    "coolant_temp": obd.commands.COOLANT_TEMP,
    "get_dtc": obd.commands.GET_DTC,
    "clear_dtc": obd.commands.CLEAR_DTC,
    "fuel_level": obd.commands.FUEL_LEVEL,
    "fuel_type": obd.commands.FUEL_TYPE,
    "vin": obd.commands.VIN
}

try:
    cmd = command in command_map
except KeyError as e:
    raise e
    
try:
    response = query(connection=connection, cmd=cmd)
except Exception as e:
    print(f"Error: {str(e)}")
    
if listen:
    while True:
        try:
            response = query(connection=connection, cmd=cmd)
            time.sleep(3)
        except Exception as e:
            print(f"Error during listen: {str(e)}")
            break
    
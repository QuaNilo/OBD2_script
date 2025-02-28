import obd
import argparse
import time
import datetime

def query(connection, cmd):
    def write_to_file(response):
        if response.value is not None:
            value_to_log = str(response.value)
        else:
            value_to_log = "No value returned"
        try:
            with open("dtc_logs", "w") as f:
                f.write(f"\n Log created on {datetime.now()}")
                f.write(response.value + "\n")
        except Exception as e:
            print(f"Failed to write to log file {str(e)}")
            
    response = connection.query(cmd)
    write_to_file(response=response)
    print(f"{response =}")
    print(f"\n{response.value =}")
    
    return response

parser = argparse.ArgumentParser()
parser.add_argument('--command', '-c', type=str, help='the command to execute', required=True)
parser.add_argument('--port', '-p', type=str, help='The OBD-II connection port (e.g., /dev/ttyUSB0 or COM3)', required=True)
parser.add_argument('--listen', '-l', action='store_true', help='If command "GET_DTC" it will listen for dtc errors', required=False)
args = parser.parse_args()

if args.listen and not args.command.lower().trim() == 'get_dtc':
    raise Exception("Listen only works with command 'get_dtc'")

connection = obd.OBD(args.port)

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
    cmd = args.command.lower() in command_map
except KeyError as e:
    raise e
    
try:
    response = query(connection=connection, cmd=cmd)
except Exception as e:
    print(f"Error: {str(e)}")
    
if args.listen:
    while True:
        try:
            response = query(connection=connection, cmd=cmd)
            time.sleep(3)
        except Exception as e:
            print(f"Error during listen: {str(e)}")
            break
    
import obd
import argparse
import time
import datetime

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
baud_rates = [500_000, 38400, 10400, 9600, 115200, 57600, 19200, 14400, 4800]
ports = obd.scan_serial()
parser = argparse.ArgumentParser()

parser.add_argument('--command', '-c', type=str, help='the command to execute', required=True)
parser.add_argument('--port', '-p', type=str, help='The OBD-II connection port (e.g., /dev/ttyUSB0 or COM3)', required=False)
parser.add_argument('--listen', '-l', action='store_true', help='If command "GET_DTC" it will listen for dtc errors', required=False)
args = parser.parse_args()

command = args.command.lower().strip()
port = args.port.strip()
listen = args.listen

if listen and not command == 'get_dtc':
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

for baud in baud_rates:
    try:
        ##USE 'baudrate' parameter IF NOT WORKING 
        connection = obd.OBD(ports[0] if not port else port, baudrate=None, fast=False, start_low_power=True)
        if connection.is_connected():
            print(f"Successfully connected using {baud} baud")
            break
        else:
            print(f"Failed to connect using {baud} baud")
    except Exception as e:
        print(f"Error trying {baud} baud: {e}")


try:
    cmd = command_map[command]
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
    
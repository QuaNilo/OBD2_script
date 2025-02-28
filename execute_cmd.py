import obd
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--command', '-c', type=str, help='the command to execute', required=True)
parser.add_argument('--port', '-p', type=str, help='The OBD-II connection port (e.g., /dev/ttyUSB0 or COM3)', required=True)
parser.add_argument('--listen', '-l', type=bool, help='If command "GET_DTC" it will listen for dtc errors', required=False)
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
    response = connection.query(cmd)
    print(f"{response =}")
    print(f"\n{response.value =}")
except Exception as e:
    print(f"Error : {str(e)}")
# OBD2 Command Executor

## Overview
This Python script allows you to execute OBD-II commands on your vehicle's ECU using an ELM327-compatible OBD-II adapter. You can query various vehicle parameters such as RPM, speed, throttle position, coolant temperature, and more. Additionally, the script supports listening for Diagnostic Trouble Codes (DTCs).

## Features
- Execute OBD-II commands and retrieve vehicle data.
- Listen for Diagnostic Trouble Codes (DTCs) when using `GET_DTC`.
- Save DTC logs to a file for later analysis.
- Support for both USB and Bluetooth OBD-II adapters.

## Requirements
- Python 3.x
- `python-OBD` library
- An ELM327-compatible OBD-II adapter
- A vehicle with an OBD-II port

## Installation
1. Install Python 3.x if not already installed.
2. Install the required Python library:
   ```sh
   pip install obd
   ```
3. Clone or download this repository.

## Usage
Run the script with the required parameters:
```sh
python obd2_executor.py -c <COMMAND> -p <OBD_PORT> [-l]
```

### Arguments
| Argument      | Short | Description |
|--------------|-------|-------------|
| `--command`  | `-c`  | The OBD-II command to execute (e.g., `rpm`, `speed`, `get_dtc`) |
| `--port`     | `-p`  | The OBD-II connection port (e.g., `/dev/ttyUSB0`, `COM3`) |
| `--listen`   | `-l`  | (Optional) Listen mode, works only with `GET_DTC` |

### Example Commands
1. Get the current RPM:
   ```sh
   python obd2_executor.py -c rpm -p /dev/ttyUSB0
   ```
2. Get the vehicle speed:
   ```sh
   python obd2_executor.py -c speed -p COM3
   ```
3. Listen for diagnostic trouble codes (DTCs):
   ```sh
   python obd2_executor.py -c get_dtc -p /dev/ttyUSB0 -l
   ```

## Supported Commands
| Command      | Description |
|-------------|-------------|
| `rpm`       | Engine RPM |
| `speed`     | Vehicle speed |
| `throttle`  | Throttle position |
| `coolant_temp` | Coolant temperature |
| `get_dtc`   | Retrieve diagnostic trouble codes (DTCs) |
| `clear_dtc` | Clear diagnostic trouble codes |
| `fuel_level`| Fuel level percentage |
| `fuel_type` | Fuel type used |
| `vin`       | Vehicle Identification Number (VIN) |

## Logging
When using `get_dtc`, the script logs detected trouble codes in `dtc_logs`:
```
Log created on 2025-02-28 12:34:56
P0420 - Catalyst System Efficiency Below Threshold (Bank 1)
```

## Troubleshooting
- **Permission Denied on `/dev/ttyUSB0`**:
  ```sh
  sudo chmod 666 /dev/ttyUSB0
  ```
- **No response from the vehicle**: Ensure the OBD-II adapter is properly connected and your vehicle is on.
- **Command not supported**: Some vehicles may not support all OBD-II commands.

## License
This project is licensed under the MIT License.

## Acknowledgments
- [python-OBD](https://github.com/brendan-w/python-OBD) for OBD-II communication.


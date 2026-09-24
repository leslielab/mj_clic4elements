from ._clic import CLiC
import serial
import json
from pathlib import Path

def is_json_file(file_path: str) -> bool:
    """Returns True if the path exists, is a file, and has a .json extension."""
    path = Path(file_path)
    return path.is_file() and path.suffix.lower() == '.json'

def validate_serial_config(file_path: str) -> bool:
    """Validates that a JSON config file contains all required keys with non-empty values."""
    
    # 1. Define the exact set of required keys
    REQUIRED_KEYS = {
        "port", "baudrate", "bytesize", "parity", "stopbits", 
        "timeout", "xonxoff", "rtscts", "dsrdtr", "writeTimeout"
    }
    
    path = Path(file_path)
    if not path.is_file():
        print(f"Error: Configuration file not found at {file_path}")
        return False

    try:
        with open(path, 'r') as file:
            data = json.load(file)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON syntax in config file - {e}")
        return False

    # 2. Check for missing keys entirely
    missing_keys = REQUIRED_KEYS - data.keys()
    if missing_keys:
        print(f"Validation Failed: Missing required keys: {list(missing_keys)}")
        return False

    # 3. Check for empty/null values (while safely allowing 0 and False)
    empty_values = (None, "")
    invalid_keys = [
        key for key in REQUIRED_KEYS 
        if data[key] in empty_values
    ]
    
    if invalid_keys:
        print(f"Validation Failed: The following keys cannot be empty or null: {invalid_keys}")
        return False

    print("Success: Configuration file is valid and complete!")
    return True

def initCLiC(path_config) -> bool:
    try:
        assert is_json_file(path_config), 'Config file is not submitted or not a json.'
        assert validate_serial_config(path_config), 'json is not properly configured. See logs.'
    except:
        print('error 1')
        return False
    
    # Translate JSON values to pySerial enums
    parity_map = {
        "N": serial.PARITY_NONE,
        "E": serial.PARITY_EVEN,
        "O": serial.PARITY_ODD,
        "M": serial.PARITY_MARK,
        "S": serial.PARITY_SPACE
    }

    bytesize_map = {
        5: serial.FIVEBITS,
        6: serial.SIXBITS,
        7: serial.SEVENBITS,
        8: serial.EIGHTBITS
    }

    stopbits_map = {
        1: serial.STOPBITS_ONE,
        1.5: serial.STOPBITS_ONE_POINT_FIVE,
        2: serial.STOPBITS_TWO
    }


    with open(path_config, "r") as f:
        config = json.load(f)

    try:

        # set as a global variable
        global clic_device
        # initiate the CLiC device
        clic_device =  CLiC(
            port=config["port"],
            baudrate=config["baudrate"],
            bytesize=bytesize_map[config["bytesize"]],
            parity=parity_map[config["parity"]],
            stopbits=stopbits_map[config["stopbits"]],
            timeout=config["timeout"],
            xonxoff=config["xonxoff"],
            rtscts=config["rtscts"],
            dsrdtr=config["dsrdtr"],
            writeTimeout=config["writeTimeout"]
        )
        # success
        print('CLiC initated.')
        return True

    except Exception as e:
        print(f"error 2\n{e}")
        return False

def deconstructCLiC() -> bool:
    try:
        assert clic_device
    except:
        print('no clic connected')

    try:
        clic_device.device.close()
        return True
    except Exception as e:
        print('Error 1')
        return False
    
def changeVoltage(target_voltage, ramp_speed) -> bool:
    try:
        assert clic_device
    except:
        print('error 1')
        return False

    try:
        clic_device.disableJoystick()
        clic_device.changeVoltage(targetVoltage=target_voltage, voltageSpeed=ramp_speed)
        return True
    except:
        print('error 2')
        return False

def disableJoystick() -> bool:
    try:
        assert clic_device
    except:
        print('error 1')
        return False

    try:
        clic_device.disableJoystick()
        return True
    except:
        print('error 2')
        return False
    
def enableJoystick() -> bool:
    try:
        assert clic_device
    except:
        print('error 1')
        return False

    try:
        clic_device.enableJoystick()
        return True
    except:
        print('error 2')
        return False
    
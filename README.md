# mj_clic4elements

Python integration of **CLIC** for **Nikon NIS-Elements**.

This project provides a simple TCP socket client script to communicate with a CLIC server directly from your Nikon Elements environment.

## Installation & Setup

### General Usage
0. Have the CLiC device plugged in and find the COM port which it lies in. The COM port should have no error signs, typically written as "⚠️" in the Windows Device Manager. 
1. Download /dist/main.exe and /dist/clic_config.json. Run main.exe
2. Press "Browse" on the left hand side, and select the configuration file. Ensure that the COM port written in the configuration file matches that which the CLiC lies on.
3. Press "Connect to CLiC"
4. Use the Home and Test button to ensure that the device is working. Use the changeVoltage button to set the CLiC to a targetVoltage with a rampRate.
5. When finished, press Quit

### Nikon Elements Integration

1. Proceed with CLiC initation via the general usage pipeline.
2. Open **Nikon NIS-Elements**.
3. Create a new Python macro/script inside Elements and paste the code.

## Nikon Elements Code Example

```python
import json
import socket


def call_server(
    class_name, method, *args, host="127.0.0.1", port=65432, **kwargs
):
    """Sends a command to the CLIC server via TCP socket.

    Args:
        class_name (str): The target server class (e.g., 'clic').
        method (str): The name of the function to execute.
        *args: Variable length argument list for the method.
        host (str): Server IP address. Defaults to "127.0.0.1".
        port (int): Server port. Defaults to 65432.
        **kwargs: Arbitrary keyword arguments for the method.

    Returns:
        dict/list/str: The parsed JSON response from the server.
    """
    # Connect to the server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))

    # Parse and send the command
    command = {
        "class": class_name,
        "method": method,
        "args": args,
        "kwargs": kwargs,
    }
    s.send(json.dumps(command).encode())

    # Receive response and close connection
    response = s.recv(4096).decode()
    s.close()

    return json.loads(response)


# ==============================================================================
# USAGE EXAMPLES
# ==============================================================================
# Uncomment and edit the lines below to trigger specific CLIC functions:

# result = call_server("clic", "enableJoystick")
# result = call_server("clic", "disableJoystick")
result = call_server("clic", "changeVoltage", 69.420, 25)
```

4. Start Elements Communication in the main.exe application
5. Running a JOBs module will execute the command written. The possible commands are shown in the example code block.

## Usage

Each API method is invoked using the `call_server` function by passing the class, method name, and required parameters.

### Available Server Classes
* `clic`: Core CLIC hardware controls.

### Example Methods
* **Enable Joystick:** `call_server("clic", "enableJoystick")`
* **Disable Joystick:** `call_server("clic", "disableJoystick")`
* **Change Voltage:** `call_server("clic", "changeVoltage", voltage_value, another_param)`

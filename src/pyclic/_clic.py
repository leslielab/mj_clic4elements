import serial
import os

class CLiC():
    """
    Library of all functions used in the process of using the CLiC device, including
    those to send commands to, set/retrieve values from CLiC device, 
    read/write text files, enable/disable joystick.

    :param 
            port="COM6",
            baudrate=9600,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=1,
            xonxoff=False, 
            rtscts =False,
            dsrdtr =False,
            writeTimeout=2  
    """
                        
    def __init__(self,  port="COM7",
                        baudrate=9600,
                        bytesize=serial.EIGHTBITS,
                        parity=serial.PARITY_NONE,
                        stopbits=serial.STOPBITS_ONE,
                        timeout=1,
                        xonxoff=False, 
                        rtscts =False,
                        dsrdtr =False,
                        writeTimeout=2):
        
        self.device = serial.Serial(
        port = port,
        baudrate = baudrate,
        bytesize = bytesize, 
        parity = parity,
        stopbits = stopbits, 
        timeout = timeout,
        xonxoff = xonxoff,
        rtscts = rtscts,
        dsrdtr = dsrdtr,
        writeTimeout = writeTimeout
        )

        #CLiC base conditions; will be changed when user inputs are read
        self.vout = 55
        self.ramprate = 10.0
        self.retractrate = 100.0
        self.vlimit = 150
        self.vretract = 90
        self.retractdelay = 2500
        self.acquiredelay = 500
        self.nummovies = 150
        self.expname = str()
        self.beamcolour = str()
    
    ### Functions for communicating with serial port
    def send_command(self, command):
        """
        Write command to serial port to be read by STM32.

        :param  command: Command to be written to serial.
        :type   command: string

        :return None:
        """
        #Write to serial twice to avoid skipping line error in firmware
        command += '\n'
        try:
            self.device.write(command.encode(encoding="ascii"))
        except serial.SerialException as e:
            print(f"Error: {e}")
        try:
            self.device.write(command.encode(encoding="ascii"))
        except serial.SerialException as e:
            print(f"Error: {e}")
            
    ### Functions for enabling/disabling joystick
    def disableJoystick(self):
        """
        Execute disablejoystick command to serial port read by STM32 
        to stop joystick from changing voltage value of CLiC device.

        :param self:

        :return None:
        """
        self.send_command("disablejoystick")

    def enableJoystick(self):
        """
        Execute enablejoystick command to serial port read by STM32 
        to let joystick change voltage value of CLiC device.

        :param self:

        :return None:
        """
        self.send_command("enablejoystick")

    # ### Functions for reading from/writing to text files
    # def readFile(self, filename):
    #     """
    #     Read and return the data for experiments from a text file as inputted by the user.

    #     :param  filename: Name of textfile that user inputs information into before running the script.
    #     :type   filename: String

    #     :return:    values read from the text file, target voltages, rates, delays, number of movies, name of experiment.
    #     :rtype:     ints, floats, string
    #     """

    #     file = open(filename + ".txt").readlines()
        
    #     for line in file:
    #         if ":" in line:
    #             try:
    #                 val = line.split(":")[-1].strip()
    #                 if not val:
    #                     raise ValueError('No value for :' + line + "in file " + filename + ".txt!")
    #                 if 'Experiment name' in line:
    #                     self.expname = str(val)
    #                 elif (not val.isnumeric()) and (not 'Beam colour' in line):
    #                     raise ValueError('Value "' + val + '" must be numerical (e.g. five -> 5)')
    #                 if 'Ramp to' in line:
    #                     self.vout = int(val)
    #                 if 'Retract by' in line:
    #                     self.vretract = int(val)
    #                 if 'Ramp rate' in line:
    #                     self.ramprate = float(val)
    #                 if 'Retract rate' in line:
    #                     self.retractrate = float(val)
    #                 if 'Delay after retract' in line:
    #                     self.retractdelay = int(val)
    #                 if 'Delay before acquiring' in line:
    #                     self.acquiredelay = int(val)
    #                 if 'Number of movies' in line:
    #                     self.nummovies = int(val)
    #             except ValueError as e:
    #                 print(e)
    #                 print("Please enter/change value and check text file name!")
    #                 input("Press enter to end the process")
    #                 exit()

    #     return self.vout, self.vretract, self.ramprate, self.retractrate, self.retractdelay, self.acquiredelay, self.nummovies
    
    # def copyFile(self, oldfilename, newfilename):
    #     """
    #     Read from the given text file and create a copy of the file under a given filename.

    #     :param  oldfilename:  Name of the text file to be read from.
    #     :type   oldfilename:  string

    #     :param  newfilename:  Name of the text file to be created and written to.
    #     :type   newfilename:  string
    #     """
    #     self.readFile(oldfilename)
    #     oldfile = open(oldfilename + ".txt").readlines()
    #     try:
    #         if os.path.isfile(newfilename + ".txt"):
    #             raise ValueError("File with name " + newfilename + ".txt already exists!")
    #         newfile = open(newfilename + ".txt", "w")
    #     except ValueError as e:
    #                 print(e)
    #                 print("Please choose another name to save text file as!")
    #                 exit() 

    #     for line in oldfile:
    #         newfile.write(line)

    # def makeFile(self, filename):
    #     """
    #     Create a new text file with information from user inputs.

    #     :param  filename:  Name of the text file to create/write to.
    #     :type   filename:  string
    #     """
    #     file = open(filename + ".txt", "w")
    #     file.write("Experiment name: " + str(self.expname) + "\n")
    #     file.write("\n")
    #     file.write("Ramp to (V): " + str(self.vout) + "\n")
    #     file.write("Retract by (V): " + str(self.vretract) + "\n")
    #     file.write("Ramp rate (V/s): " + str(self.ramprate) + "\n")
    #     file.write("Retract rate (V/s): " + str(self.retractrate) + "\n")
    #     file.write("Delay after retract (ms): " + str(self.retractdelay) + "\n")
    #     file.write("Delay before acquiring (ms): " + str(self.acquiredelay) + "\n")
    #     file.write("Number of movies to take: " + str(self.nummovies) + "\n")
    #     file.write("Beam colour(s): " + str(self.beamcolour) + "\n")

    # def userInput(self):
    #     """
    #     Request and read specified experiment parameters from direct user input in terminal.

    #     :param  None:
    #     """
    #     print("All fields must have values to proceed!")
    #     self.expname = input("Experiment name: ")
    #     self.beamcolour = input("Beam colour(s): ")
    #     self.vout = input("Ramp to (V): ")
    #     self.vretract = input("Retract by (V): ")
    #     self.ramprate = input("Ramp rate (V/s): ")
    #     self.retractrate = input("Retract rate (V/s): ")
    #     self.retractdelay = input("Delay after retract (ms): ")
    #     self.acquiredelay = input("Delay before acquiring (ms): ")
    #     self.nummovies = input("Number of movies to take: ")

    # def confirmInput(self, filename):
    #     """
    #     Read from a file and print each line, prompt user for changes to be made.

    #     :param  filename:  Name of the text file to check contents of.
    #     :type   filename:  string

    #     :return:    Confirmation of if the file contents should stay the same.
    #     :rtype:     bool
    #     """
    #     print("Please confirm the following information: ")
    #     file = open(filename + ".txt").readlines()
    #     for line in file:
    #         print(line)
    #     confirm = None
    #     while confirm not in {"Y", "YES", "N", "NO"}:
    #         confirm = input("Proceed with this information? (Y/N) ").upper()
    #     if confirm == "Y" or confirm == "YES":
    #         return True
    #     return False
    
    # def findRecent(self, folder_path, type):
    #     most_recent_file = None
    #     most_recent_time = 0
    #     for entry in os.scandir(folder_path):
    #         if type == 0:
    #             if entry.is_dir():
    #                 mod_time = entry.stat().st_mtime_ns
    #                 if mod_time > most_recent_time:
    #                     most_recent_file = entry.name
    #                     most_recent_time = mod_time
    #         else:
    #             if entry.is_file():
    #                 mod_time = entry.stat().st_mtime_ns
    #                 if mod_time > most_recent_time:
    #                     most_recent_file = entry.name
    #                     most_recent_time = mod_time
    #     return most_recent_file

    ### Functions for the CLiC/unCLiC process
    def changeVoltage(self, targetVoltage, voltageSpeed):
        """
        Increase voltage by rampSpeed to reach targetVoltage by
        sending commands to serial port to be read by STM32.

        :param  targetVoltage:  Voltage for CLiC device to reach.
        :type   targetVoltage:  float

        :param  voltageSpeed:  Speed (V/s) of the changing voltage.
        :type   voltageSpeed:  float

        :return None:
        """
        commandvrate = "vrate=" + str(voltageSpeed)
        commandvout = "vout=" + str(targetVoltage)

        self.send_command(commandvrate)
        self.send_command(commandvout)

    ### Functions for getting CLiC values or information
    def getVrate(self):
        """
        Print value currently saved as vrate in CLiC.

        :param  self:
        :return None:
        """
        command = "vrate?"
        self.send_command(command)

    def getVlimit(self):
        """
        Print value currently saved as vlimit in CLiC.

        :param  self:
        :return None:
        """
        command = "vlimit?"
        self.send_command(command)
    
    def getVout(self):
        """
        Print value currently saved as vout in CLiC.

        :param  self:
        :return None:
        """
        command = "vout?"
        self.send_command(command)
    
    def getCommands(self):
        """
        Print all possible commands.

        :param  self:
        :return None:
        """
        command = "help"
        self.send_command(command)

    def getID(self):
        """
        Print product ID.

        :param  self:
        :return None:
        """
        command = "id?"
        self.send_command(command)
    
    def getSerialNo(self):
        """
        Print serial number.

        :param  self:
        :return None:
        """
        command = "serial?"
        self.send_command(command)

    def getFirmware(self):
        """
        Prints firmware version.

        :param  self:
        :return None:
        """
        command = "firmware?"
        self.send_command(command)

    ### Functions for setting CLiC values
    def setVrate(self, val):
        """
        Set value of vrate in CLiC.

        :param  self:

        :param val: number to set vrate to.
        :type val:  int

        :return None:
        """
        command = "vrate="+val
        self.send_command(command)

    def setVlimit(self, val):
        """
        Set value of vlimit in CLiC.

        :param  self:

        :param val: number to set vlimit to.
        :type val:  int

        :return None:
        """
        command = "vlimit="+val
        self.send_command(command)
    
    def setVout(self, val):
        """
        Set value of vout in CLiC.

        :param  self:

        :param val: number to set vout to.
        :type val:  int

        :return None:
        """
        command = "vout="+val
        self.send_command(command)


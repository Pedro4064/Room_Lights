from datetime import datetime
import RPi.GPIO as GPIO
import requests
import json
import time

class RaspberryPi():

    def __init__(self):

        # The path for the json file
        self.__file_path = '/home/pi/Desktop/Room_Lights/status.json'

        # The url to the flask application
        self.url = 'http://192.168.15.13:5000/updateStatus'

        # Status variables
        self.lights_on = True
        self.color_name = ''
        
        # initialize the raspberry pi's GPIOs acorinding to the board's numbering
        GPIO.setmode(GPIO.BOARD)

        # Set the gpios as outputs
        self.red_gpio   = 18
        self.blue_gpio  = 11
        self.green_gpio = 15

        GPIO.setup(18, GPIO.OUT)
        GPIO.setup(11, GPIO.OUT)
        GPIO.setup(15, GPIO.OUT)


        self.timer_on = False
        self.timer_checked = False
        self.timer_turned_on = 0
        self.timer_off = 0
        self.sleep_time = 0

        self.wake_lights_on = True
        self.wake_lights_time = ''

    def __parse_json_data(self):
        
        # Read the data in the file
        with open(self.__file_path, 'r') as json_file:

            # load the data using the json module
            json_data = json.loads(json_file.read())

        # return the json data
        return json_data

    def __control_lights(self, rbg_values):

        # Raspberry pi commands to set the GPIOs HIGH or LOW
        print(json.dumps(rbg_values, indent=1))

        # Red chanel
        if rbg_values['R'] != 255:

            # turn it off
            GPIO.output(self.red_gpio, False)
        else:

            # Turn on the red chanel
            GPIO.output(self.red_gpio, True)

        # Green chanel
        if rbg_values['G'] != 255:
            GPIO.output(self.green_gpio, False)
        else:
            GPIO.output(self.green_gpio, True)
        
        # Blue chanel
        if rbg_values['B'] != 255:
            GPIO.output(self.blue_gpio, False)
        else:
            GPIO.output(self.blue_gpio, True)
        
    def __make_post_request(self, header:'The item you are sending', payload:'The json data'):

        # Format the payload
        data = {header: payload}

        # Make the post request
        request = requests.post(self.url, json = data, headers = {'Content-type': 'application/json'})

    def __get_current_time(self):

        # Get a datetime object
        time = datetime.now().time()

        # Make a string of the info on the instance
        time = str(time)

        # Format the string into a list
        time = time.split(':')

        # Get the minutes and hour
        time = {"hour": int(time[0]), 'minutes': int(time[1])}

        # return the dictionary containing the data
        return time

    def update_status(self):
         
        #  Get the parsed data
        self.json_data = self.__parse_json_data()
    
        # update the instance's variables
        self.lights_on = self.json_data.get("On")
        self.color_name = self.json_data.get("color_name")
        self.timer_on = self.json_data.get("Sleep").get("Timer")
        self.sleep_time = self.json_data.get("Sleep").get("Time")
        self.wake_lights_on = self.json_data.get("Wake Time").get("wake")
        self.wake_lights_time = self.json_data.get("Wake Time").get('time')

        
        # print(self.wake_lights_time)
        print(json.dumps(self.json_data, indent=4))

    def update_lights(self):

        # Check to see if they are on or off
        if self.lights_on :

            # Get the whole color dictionary
            rbg_values = self.json_data.get("Settings").get("color").get("color_option")

            # Get the dictionary for the specific color
            rbg_values = rbg_values.get(self.color_name)

            # Change the GPIO values
            self.__control_lights(rbg_values = rbg_values)

        else:

            self.__control_lights(rbg_values={'R' : 0, 'B' : 0, 'G' : 0})

    def check_timer(self):

        # If the timer is set to on, update the status
        if self.timer_on == True and self.timer_checked == False:

            # Get the time the user whishes to turn the lights off and subtract one -> So there is no the lights turn off one minute before the stablished time
            self.sleep_time -= 1
            self.timer_checked = True

            # Get the time which the timer function was enabled 
            self.timer_turned_on = self.__get_current_time()['minutes']
            
            # Calculate the minute in which the lights should be turned off
            self.timer_off = self.timer_turned_on + self.sleep_time

            # If it is grater than 60, it means it is in the next hour that the lights should be off, so subtaract 60 from it
            if self.timer_off >= 60:
                self.timer_off = self.timer_off - 60

            print('Ligts will be off by', self.timer_off)
                
        # If the timer was checked and it is turned on, check the time, if it matches the one on the file, turn off the lights
        elif self.timer_checked:

            # Check if the time is the one set to turn off the lights
            current_time = self.__get_current_time()

            # If the current minute is the same as the one set to turn the lights off, do so
            if current_time['minutes'] == self.timer_off:

                # Turn off the lights
                self.__control_lights({'R' : 0, 'G' : 0, 'B' : 0 })
                
                # update the variables
                self.__make_post_request(header = "Sleep", payload = {"Timer": False} )
                self.__make_post_request(header = 'On', payload = False)

                # wait for the update to reach the server
                time.sleep(5)

                self.timer_checked = False

    def wake_up_lights(self) :

        # if the option to wake up is on, get the time which it should be turned on
        if self.wake_lights_on:

            # Get the current time
            time = self.__get_current_time()

            # parse the time on the json file
            self.wake_lights_time = self.wake_lights_time.split(':')

            # If the hours match, check the minutes
            if time['hour'] == int(self.wake_lights_time[0]):

                # Check the minutes
                if time['minutes'] == int(self.wake_lights_time[1]):

                    # turn on the lights
                    self.__control_lights(rbg_values = {'R':255, 'G':255, 'B':255})

                    # update the server
                    self.__make_post_request(header='On', payload=True)
        

# Instanciate the raspberry pi class
rPi = RaspberryPi()

while True:

    # Read the file and update local variables
    rPi.update_status()

    # Check to see if the timer is on, and if it is check to see if it is time to turn the lights off
    rPi.check_timer()

    # update the lights 
    rPi.update_lights()

    # Check to see if it is wake up time already
    rPi.wake_up_lights()

    # wait for 3 seconds before checking again
    time.sleep(1)

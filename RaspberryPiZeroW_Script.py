from datetime import datetime
import requests
import json
import time

class RaspberryPi():

    def __init__(self):

        # The path for the json file
        self.__file_path = '/Users/pedrocruz/Desktop/Programming/Python/Git/Room_lights/Room-Lights/status.json'

        # The url to the flask application
        self.url = ''

        # Status variables
        self.lights_on = True
        self.color_name = ''
        
        self.timer_on = False
        self.timer_checked = False
        self.timer_turned_on = 0
        self.timer_off = 0
        self.sleep_time = 0

        self.wake_lights_on = True
        self.wake_lights_time = ''

        self.red   = 255
        self.blue  = 255
        self.green = 255

    def __parse_json_data(self):
        
        # Read the data in the file
        with open(self.__file_path, 'r') as json_file:

            # load the data using the json module
            json_data = json.loads(json_file.read())

        # return the json data
        return json_data

    def __control_lights(self, rbg_values):

        # Raspberry pi commands to set the pwm duty cycles
        pass 

    def __make_post_request(self, header:'The item you are sending', payload:'The json data'):

        # Format the payload
        data = json.dumps({header: payload})

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

        
        print(self.wake_lights_time)
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
            if self.timer_off > 60:
                self.timer_off = self.timer_off - 60


                
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
            
                self.timer_checked = False

        
# if __name__ == "__main__":
counter = 0

# Instanciate the raspberry pi class
rPi = RaspberryPi()

while True:

    # Read the file and update local variables
    rPi.update_status()

    # Check to see if the timer is on, and if it is check to see if it is time to turn the lights off
    rPi.check_timer()

    # wait for 3 seconds before checking again
    time.sleep(3)
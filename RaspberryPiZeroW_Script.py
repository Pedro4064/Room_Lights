import requests
import json

class RaspberryPi():

    def __parse_json_data(self, raw_data):

        # Parse the json data and return a dict with all the parsed data
        parsed_json_data = json.loads(raw_data)

        # Work on parsing the data and getting trash out

        # Return the parsed and clean json data
        return parsed_json_data

    def get_request(self):

        # The url from pythonanywhere that will be hosting the flask web app
        self.url = ''
        
        # Make a get request and get the json data from the server
        self.json_data = requests.get(self.url)

        # Parse the data
        self.json_data = self.__parse_json_data(self.json_data)
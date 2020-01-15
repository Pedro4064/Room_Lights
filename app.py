import requests
from flask import Flask, request
import json
import time

app = Flask(__name__)
file_path = '/home/pedro/Documents/Python/Room_Lights/status.json'

app.route('/')
def ok():

    return 'ok'
    
app.route("/updateStatus", methods = ['POST'])
def update():

    # global variable
    global file_path

    # The key sent from the phone to the server, as an auth pin
    https_key = 'Pedro4064'

    # Get the json data containing the new lamp state(on or off)
    data = request.get_json()#.get(https_key)

    # Get the dict key, to know which data the user whishes to change
    data_type = list(data.keys())[0]


    # Get the data in the file on the system
    file_data = json.loads(get_status())


    # if the data is not the same, update the data on disk
    if data == file_data:

        # update the dict that was extracted on disk
        file_data[data_type] = data[data_type]


        # open the data file in write mode
        with open(file_path,'w') as file:

            # Write the data to the file
            file.write(json.dumps(file_data, indent = 4))


app.route("/getStatus", methods = ['GET'])
def get_status():

    # global variable
    global file_path
    
    # Open and read the file
    with open(file_path, 'r') as data:

        # load the data in the file as a list/dictionaries
        json_data = json.loads(data.read())
        print(json.dumps(json_data, indent=4))
    # Return the json data as a string
    return json.dumps(json_data, indent=4)

if __name__ == "__main__":

    app.run(debug = True)
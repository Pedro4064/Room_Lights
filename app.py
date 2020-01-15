import requests
from flask import Flask, request
import json
import time

app = Flask(__name__)
file_path = '/Users/pedrocruz/Desktop/Programming/Python/Git/Room_lights/Room-Lights/status.json'

    
@app.route("/updateStatus", methods = ['POST'])
def update():

    # global variable
    global file_path

    # The key sent from the phone to the server, as an auth pin
    # https_key = 'Pedro4064'

    # Get the json data containing the new lamp state(on or off)
    data = request.get_json()#.get(https_key)
    print('New Data:',json.dumps(data, indent=4))

    # Get the dict key, to know which data the user whishes to change
    data_type = list(data.keys())[0]
    print('Data Type:',data_type)

    # Get the data in the file on the system
    file_data = json.loads(get_status())


    # if the data is not the same, update the data on disk
    if data != file_data:

        # update the dict that was extracted on disk
        file_data[data_type] = data[data_type]
        print(data[data_type])

        # open the data file in write mode
        with open(file_path,'w') as file:

            # Write the data to the file
            file.write(json.dumps(file_data, indent = 4))

    return 'Updated'

@app.route("/getStatus", methods = ['GET'])
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

@app.route("/colorOptions", methods = ['GET'])
def get_colors():

    # read the file
    data = json.loads(get_status())

    color_options = data['Settings']['color']['color_option']
    print(color_options)

    return json.dumps(color_options)

if __name__ == "__main__":

    app.run(debug = True)
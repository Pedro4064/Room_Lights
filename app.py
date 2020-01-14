import requests
from flask import Flask, request
import time

app = Flask(__name__)


app.route("/updateStatus", methods = ['POST'])
def update():

    # The key sent from the phone to the server, as an auth pin
    https_key = 'Pedro4064'

    # Get the json data containing the new lamp state(on or off)
    data = request.get_json().get(https_key)






app.run(debug = True)
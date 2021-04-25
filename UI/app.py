from flask import Flask, render_template, redirect, url_for
from firebase import firebase
import json
import pyrebase
config ={
    "apiKey": "AIzaSyDayX_x5iFPmISVEFfXdthSU3KtC2aA3yY",
    "authDomain": "house-9f5c0.firebaseapp.com",
    "databaseURL": "https://house-9f5c0-default-rtdb.firebaseio.com",
    "projectId": "house-9f5c0",
    "storageBucket": "house-9f5c0.appspot.com",
    "messagingSenderId": "332253329742",
    "appId": "1:332253329742:web:405f2312e1d5eb3c07061f",
    "measurementId": "G-9SJTS7BFS1"
}
firebase = pyrebase.initialize_app(config)
db = firebase.database()

app = Flask(__name__)

@app.route("/")
def index():
    result = db.child('Realtor').get().val()
    result1 = db.child('Crime').get().val()
    #result2 = get_crime_info(result1)
    return render_template('index.html', result=result, result1= result1)


def get_crime_info(obj):
    json_data = json.dumps(obj)
    dict_data = json.loads(json_data)
    crime_data_list = list()
    for index in range(0, len(dict_data)):
        if("chance_crime" not in dict_data[index].keys()):
            dict_data[index]['chance_crime'] = None
        if("city" not in dict_data[index].keys()):
            dict_data[index]['city'] = None
        if("crime_rate" not in dict_data[index].keys()):
            dict_data[index]['crime_rate'] = None
        if("state" not in dict_data[index].keys()):
            dict_data[index]['state'] = None
        i = {}
        i.setdefault("chance_crime", None)
        i.setdefault("city", None)
        i.setdefault("crime_rate", None)
        i.setdefault("state", None)
        chance_crime = dict_data[index]['chance_crime']
        city = dict_data[index]['city']
        crime_rate = dict_data[index]['crime_rate']
        state = dict_data[index]['state']
        i["chance_crime"] = chance_crime
        i["city"] = city
        i["crime_rate"] = crime_rate
        i["state"] = state
        crime_data_list.append(i)
    return crime_data_list

if __name__ == "__main__":
    app.run(debug=True)
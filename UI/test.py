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
result = db.child('Realtor').get().val()
result1 = db.child('Crime').get().val()
print(result1)
from flask import Flask,request
from SmartParking.MongoClient import MongoWrapper
from flask_cors import CORS
from SmartParking.ErrorCodes import Codes
from SmartParking.res import Constant
import json

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

db=MongoWrapper.MongoDataBase(host=Constant.host,port=Constant.mongodb_port)


@app.route('/register', methods = ['POST','GET'])
def register():
    if request.method == 'GET':
        return Codes.invalidrequestMethod()
    if request.method == 'POST':
        return db.registeruser(request.get_json())

@app.route('/login', methods = ['POST','GET'])
def login():
    if request.method == 'GET':
        return Codes.invalidrequest()
    if request.method == 'POST':
        return db.loginuser(request.get_json())

@app.route('/addmoney', methods = ['POST','GET'])
def addmoney():
    if request.method == 'GET':
        return Codes.invalidrequest()
    if request.method == 'POST':
        return db.addMoney(request.get_json())

@app.route('/getdevicedata', methods = ['POST', 'GET'])
def getdevicedata():
    if request.method == 'GET':
        return Codes.invalidrequest()
    if request.method == 'POST':
        return db.getDeviceData(request.get_json())

@app.route('/registerdevice', methods = ['POST', 'GET'])
def registerdevice():
    if request.method == 'GET':
        return Codes.invalidrequest()
    if request.method == 'POST':
        return db.registerDevice(request.get_json())

@app.route('/getallparkingspots', methods = ['POST', 'GET'])
def getallparkingspots():
    if request.method == 'POST':
        return Codes.invalidrequestMethod()
    if request.method == 'GET':
        return db.getAllParkingSpots()

@app.route('/bookparkingspot', methods = ['POST', 'GET'])
def bookparkingspot():
    if request.method == 'GET':
        return Codes.invalidrequestMethod()
    if request.method == 'POST':
        return db.bookParkingSpot(request.get_json())

@app.route('/getparkingspaces', methods = ['POST', 'GET'])
def getparkingspaces():
    if request.method == 'POST':
        return Codes.invalidrequestMethod()
    if request.method == 'GET':
        return db.getParkingSpaces()

@app.route('/getparkingspotbyid', methods = ['POST', 'GET'])
def getparkingspotbyid():
    if request.method == 'GET':
        return Codes.invalidrequestMethod()
    if request.method == 'POST':
        return db.getParkingSpotById(request.get_json())

@app.route('/endbooking', methods = ['POST', 'GET'])
def endbooking():
    if request.method == 'GET':
        return Codes.invalidrequestMethod()
    if request.method == 'POST':
        return db.endBooking(request.get_json())



if __name__ == '__main__':
    app.run(host="10.20.3.65",port=8000)


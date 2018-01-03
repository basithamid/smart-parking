from pymongo import MongoClient
import datetime
from SmartParking.ErrorCodes import Codes
import json
from bson.json_util import dumps
from pymongo.errors import DuplicateKeyError
class MongoDataBase:
    db=None

    def __init__(self,host,port):
        client = MongoClient(host=host, port=port)
        client=client
        self.db = client.parkingDB

    def registeruser(self,data):
        userdb=self.db.userdb
        if 'password' in data and 'email' in data and 'name' in data:
            try:
                id=dumps(userdb.insert_one({"password":data["password"],"email":data["email"],"name":data["name"],"money":0}).inserted_id)
                return json.dumps({"status":"success","message":{"email":data["email"],"name":data["name"]}})
            except DuplicateKeyError:
                return Codes.userAlreadyExist()
        else:
            return Codes.badRequest()

    def loginuser(self, data):
        userdb = self.db.userdb
        if 'password' in data and 'email' in data :
                record = dumps(userdb.find_one({"email": data["email"]}))
                record= json.loads(record)
                print(record)
                if record is None:
                    return Codes.invalidEmail()
                elif data["password"] == record["password"] :
                    return json.dumps({"status": "success", "message": {"email": data["email"],"name": record["name"]}})
                else:
                    return Codes.invalidPassword()
        else:
            return Codes.badRequest()


    def addMoney(self,data):
        userdb=self.db.userdb
        if 'email' in data and 'amount' in data :
                id=dumps(userdb.update({"email":data["email"]},{'$inc': {'money': int(data["amount"])}}))
                id=json.loads(id)
                print(id)
                if id['updatedExisting'] == True:
                    return json.dumps({"status":"success","message":{"email":data["email"]}})
                else:
                    return Codes.invalidEmail()
        else:
            return Codes.badRequest()

    def deductMoney(self,data):
        userdb=self.db.userdb
        if 'email' in data and 'amount' in data :
                id=dumps(userdb.update({"email":data["email"]},{'$inc': {'money': - int(data["amount"])}}))
                id=json.loads(id)
                print(id)
                if id['updatedExisting'] == True:
                    return json.dumps({"status":"success","message":{"email":data["email"]}})
                else:
                    return Codes.invalidEmail()
        else:
            return Codes.badRequest()

    def registerDevice(self,data):
        devicedb = self.db.devicedata
        if 'serial_number' in data and 'name' in data and 'lat' in data and 'long' in data and 'owner' in data and 'address' in data:
            record = dumps(devicedb.find_one({'serial_number':data['serial_number']}))
            record = json.loads(record)
            if record is None:
                return Codes.invalidDevice()
            else:
                record = dumps(devicedb.update({"serial_number":data["serial_number"]}, {'$set': {'name':data['name'], 'lat':data['lat'], 'long':data['long'], 'owner':data['owner'], 'address': data['address']}}, False, True))
                record = json.loads(record)
                print(record)
                if record['updatedExisting'] == True:
                    return json.dumps({"status":"success","message":{"serial_number":data["serial_number"], 'name':data['name'], 'lat':data['lat'], 'long':data['long'], 'owner':data['owner'], 'address': data['address']}})
                else:
                    return Codes.invalidDevice()
        else:
            return Codes.badRequest()


    def onDeviceData(self,serial_number,status):
        devicedb=self.db.devicedata
        result= devicedb.update({'serial_number': serial_number},{'$set': {'status': status}}, upsert=False)
        print(result['updatedExisting'])
        if result['updatedExisting'] is False:
            try:
                devicedb.insert_one({'serial_number': serial_number,"status":status,"acknowledged":False,"booked":False})
            except DuplicateKeyError:
                print("Error in inserting new Record")



    def getDeviceData(self, data):
        if 'serial_number' in data:
            devicedb = self.db.devicedata
            record = dumps(devicedb.find_one({"serial_number":data["serial_number"]}))
            record  = json.loads(record)
            print(record)
            if record is None:
                return Codes.invalidDevice()
            else:
                return json.dumps({"status":"success", "message": {"serial_number":record['serial_number'], "status": record["status"], "booked":record["booked"]}})
        else:
           return Codes.badRequest()


    def getAllParkingSpots(self):
        devicedb = self.db.devicedata
        records = dumps(devicedb.find())
        records = json.loads(records)
        if records is None:
            return Codes.noParkingSpotsFound()
        else:
            return json.dumps({"status":"success", "message": {"records": records}})

    def bookParkingSpot(self, data):
        if "serial_number" in data and "email" in data:
            devicedb = self.db.devicedata
            time = datetime.datetime.now().strftime("%H:%M:%S")
            record = dumps(devicedb.update({"serial_number": data["serial_number"]}, {
                    '$set': {'booked':data['email'], 'booked_start_time': time, 'rate': 5}},
                                               False, True))
            record = json.loads(record)
            print(record)
            if record['updatedExisting'] == True:
                record = dumps(devicedb.find_one({"serial_number": data["serial_number"]}))
                record = json.loads(record)
                return json.dumps({"status":"success","message":{"serial_number":record['serial_number'], 'name':record['name'], 'lat':record['lat'], 'long':record['long'], 'owner':record['owner'], 'booked_start_time': record['booked_start_time']}})
            else:
                return Codes.invalidDevice()
        else:
            return Codes.badRequest()


    def getParkingSpaces(self):
        devicedb = self.db.devicedata
        records = dumps(devicedb.find())
        records = json.loads(records)
        if records is None:
            return Codes.noParkingSpacesFound()
        else:
            return json.dumps({"status": "success", "message": {"records":records}})

    def getParkingSpotById(self,data):
        if 'serial_number' in data:
            devicedb = self.db.devicedata
            record = dumps(devicedb.find_one({"serial_number": data["serial_number"]}))
            record = json.loads(record)
            if record is None:
                return Codes.noParkingSpotsFound()
            else:
                return json.dumps({"status": "success", "message": {"record": record}})
        else:
            return Codes.badRequest()

    def endBooking(self, data):
        if 'serial_number' in data:
            devicedb = self.db.devicedata
            end_time = datetime.datetime.now().strftime("%H:%M:%S")
            record = dumps(devicedb.find_one({"serial_number": data["serial_number"]}))
            record = json.loads(record)
            print(record['booked'])
            if record is None:
                return Codes.invalidDevice()
            else:
                parked_time = int(end_time[0:2]) - int(record['booked_start_time'][0:2])
                amount = (1 + parked_time) * 10
                self.addMoney({"email": record["owner"], "amount": amount})
                self.deductMoney(({"email": record["booked"], "amount": amount}))
                record = dumps(devicedb.update({"serial_number": record["serial_number"]},
                                                       {"$set": {"booked_start_time": "00",
                                                                 "booked": "false"}},
                                                       False, True))
                record = json.loads(record)
                if record['updatedExisting'] == True:
                    return json.dumps({"status": "success", "message": { "amount": amount}})
                else:
                    return Codes.invalidDevice()
        else:
            return Codes.badRequest()


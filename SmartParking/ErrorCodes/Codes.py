import json
def invalidrequestMethod():
    return json.dumps({"status":"error","message":{"code":"405","error":"Method Not Allowed"}})


def invalidURl():
    return json.dumps({"status": "error", "message": {"code": "204", "error": "No Content"}})

def badRequest():
    return json.dumps({"status": "error", "message": {"code": "400", "error": "Bad Request"}})

def userAlreadyExist():
    return json.dumps({"status": "error", "message": {"code": "800", "error": "User Already Exist"}})

def invalidEmail():
    return json.dumps({"status": "error", "message": {"code": "801", "error": "Invalid Email"}})

def invalidPassword():
    return json.dumps({"status": "error", "message": {"code": "802", "error": "Invalid Password"}})

def invalidDevice():
    return json.dumps({"status": "error", "message": {"code": "803", "error": "Invalid Device"}})

def noParkingSpotsFound():
    return json.dumps({"status": "error", "message": {"code": "804", "error": "No Device Found"}})

def noParkingSpacesFound():
    return json.dumps({"status": "error", "message": {"code": "805", "error": "No Parking Spot Found"}})
from flask import *
from flask_restful import Resource, Api
from pymongo import *
import os

app = Flask(__name__)
api = Api(app)

db_uri = os.getenv("MONGODB_URI", 'mongodb://mongodb:27017/')


client = MongoClient(db_uri)
db = client.LearnMOngodb


class Login(Resource):
    def post(self):
        try:
            collectionss = db.testCollections
            username = request.json["username"]
            password = request.json["password"]
            response = collectionss.find_one({"username": username, "password": password})
            if response is not None:
                return make_response(json.dumps({'Msg': 'Login Successfully'}), 200)
            else:
                return make_response(json.dumps({'Msg': 'Login not Successfully'}), 200)
        except:
            return make_response(json.dumps({'Msg': 'Internal Server Error'}), 500)


class Register(Resource):
    def post(self):
        try:
            collections = db.testCollections
            username = request.json["username"]
            password = request.json["password"]
            emailid = request.json["emailid"]
            phonenumber = request.json["phonenumber"]
            response = collections.find_one({"username": username})
            if response is None:
                result = collections.insert({
                    "username": username, "password": password, "emailid": emailid, "phonenumber": phonenumber
                })
                if result is not None:
                    return make_response(json.dumps({'Msg': 'Inserted Successfully'}), 200)
                else:
                    return make_response(json.dumps({'Msg': 'Inserted not Successfully'}), 200)
            else:
                return make_response(json.dumps({"Msg": "User already Exists"}), 200)
        except:
            return make_response(json.dumps({'Msg': 'Internal Server Error'}), 500)


class ChangePassword(Resource):
    def post(self):
        try:
            collections = db.testCollections
            username = request.json["username"]
            password = request.json["password"]
            newpassword = request.json["passwordd"]
            response = collections.find_one({"username": username, "password": password})
            if response is not None:
                result = collections.update_one({"password": password}, {"$set": {"password": newpassword}})
                if result is not None:
                    return make_response(json.dumps({'Msg': 'Password Changed Successfully'}), 200)
                else:
                    return make_response(json.dumps({'Msg': 'Password Not Changed Successfully'}), 200)
        except:
            return make_response(json.dumps({'Msg': 'Internal Server Error'}), 500)


class ForgetPassword(Resource):
    def post(self):
        try:
            collections = db.testCollections
            username = request.json["username"]
            newpassword = request.json["passwordd"]
            response = collections.find_one({"username": username})
            if response is not None:
                result = collections.update_one({"username": username}, {"$set": {"password": newpassword}})
                if result is None:
                    return make_response(json.dumps({'Msg': 'Result Not Added Successfully'}), 500)
                else:
                    return make_response(json.dumps({"Msg": "Result Added Successfully"}), 200)
        except:
            return make_response(json.dumps({'Msg': 'Internal Server Error'}), 500)


class deleteUser(Resource):
    def post(self):
        try:
            collections = db.testCollections
            username = request.json["username"]
            response = collections.find_one({"username": username})
            if response is None:
                result = collections.delete_one({"username": username})
                if result is None:
                    return make_response(json.dumps({"Msg": "Internal Server Error"}), 500)
        except:

            return make_response(json.dumps({"Msg": "Internal Server Error"}), 500)


class AddRole(Resource):
    def post(self):
        try:
            collectionss = db.role
            collections = db.testCollections
            username = request.json["username"]
            role_name = request.json["rolename"]
            result = collections.find_one({"username": username})
            print(type(result))
            if result is not None:
                response = collectionss.find_one({"rolename": role_name})
                if response is not None:
                    responsee = collections.update_one({"username": username}, {"$set": {"role": role_name}})
                    if responsee is not None:
                        return make_response(json.dumps({"Msg": "Role Assigned successfully"}), 200)
                    else:
                        return make_response(json.dumps({"Msg": "Role Not Assigned yet"}), 200)
            else:
                return make_response(json.dumps({"Msg": "User not Exists"}), 200)

        except:
            return make_response(json.dumps({"Msg": "Internal Server Error"}), 500)


class Userdeleterole(Resource):
    def post(self):
        try:
            collections = db.testCollections
            username = request.json["username"]
            rolename = request.json["rolename"]
            result = collections.find_one({"username": username})
            if result is not None:
                response = collections.update_one({"username": username}, {"$unset": {"role": rolename}})
                if response is not None:
                    return make_response(json.dumps({"Msg": "Role Unassigned Succcesfully"}), 200)
                else:
                    return make_response(json.dumps({"Msg": "Role is not assigned to the specfic username"}), 200)
            else:
                return make_response(json.dumps({"Msg": "User not exist"}), 200)
        except:
            return make_response(json.dumps({"Msg": "Internal Server Error"}), 500)


class DeleteRole(Resource):
    def post(self):
        try:
            collections = db.role
            collectionss = db.testCollections
            rolename = request.json["rolename"]
            result = collections.find({"rolename": rolename})
            if result is not None:
                response = collections.delete_one({"rolename": rolename})
                if response is not None:
                    for i in collectionss.find({"role": rolename}):
                        if i["role"] == rolename:
                            print("jdjshabhdgb")
                            resultt = collectionss.update_one({"username": i["username"]}, {"$unset": {"role": ""}})
                    else:
                        return make_response(json.dumps({"Msg": "No such role with username exists...."}), 200)
            else:
                return make_response(json.dumps({"Role Doesn't Exists"}), 200)
        except:
            return make_response(json.dumps({"Msg": "Internal Servel Error"}), 200)


api.add_resource(Userdeleterole, "/deleteuserrole")
api.add_resource(DeleteRole, "/deleterole")
api.add_resource(AddRole, "/addrole")
api.add_resource(deleteUser, "/deleteUser")
api.add_resource(Login, '/login')
api.add_resource(Register, "/register")
api.add_resource(ChangePassword, "/changepassword")
api.add_resource(ForgetPassword, "/ForgetPassword")

# driver function
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8000))
    app.run(host='0.0.0.0', port=port, debug=True)

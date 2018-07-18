import sqlite3
from flask_restful import Resource, reqparse
from fields import USER_TABLE
from models.user import UserModel

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', 
        required=True,
        help="Username is required."
    )
    parser.add_argument('password', 
        required=True,
        help="Password is required."
    )
    
    def post(self):
        data = UserRegister.parser.parse_args()
        
        if UserModel.find_by_username(data['username']):
            return {
                "message": 'User is already existed.'
            }, 400
            
        user = UserModel(**data)
        user.save_to_db()

        return {
            'message': "User has been create successfully!"
        }, 201
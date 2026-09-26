from flask_restful import reqparse, abort, Resource
from . import db_session
from .user import Users
from flask import jsonify
from datetime import datetime

parser = reqparse.RequestParser()
parser.add_argument('login', required=True)
parser.add_argument('name', required=True)
parser.add_argument('email', required=True)
parser.add_argument('photo', required=True)
parser.add_argument('password', required=True)


class UsersResource(Resource):
    def get(self, users_id):
        abort_if_users_not_found(users_id)
        session = db_session.create_session()
        users = session.query(Users).get(users_id)
        return jsonify({'users': users.to_dict(
            only=('id', 'login', 'name', 'email', 'photo', 'created_date'))})

    def delete(self, users_id):
        abort_if_users_not_found(users_id)
        session = db_session.create_session()
        users = session.query(Users).get(users_id)
        session.delete(users)
        session.commit()
        return jsonify({'success': 'OK'})


class UsersListResources(Resource):
    def get(self):
        session = db_session.create_session()
        users = session.query(Users).all()
        return jsonify(
            {'users': [user.to_dict(only=('id', 'login', 'name', 'email', 'photo', 'created_date')) for user in users]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        users = Users(
            login=args['login'],
            name=args['name'],
            email=args['email'],
            photo=args['photo'],
            created_date=datetime.now(),
        )
        users.set_password(args['password'])
        session.add(users)
        session.commit()
        return jsonify({'id': users.id})


def abort_if_users_not_found(users_id):
    session = db_session.create_session()
    users = session.query(Users).get(users_id)
    if not users:
        abort(404, message=f"News {users_id} not found")
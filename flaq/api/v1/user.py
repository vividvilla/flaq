from flask.ext.restful import Resource, marshal_with
from flask.ext.login import login_user, current_user

from flaq.utils import verify_password
from flaq.models.user import User
from common import user_existance_check, Parsers, \
        verify_client, client_validate, OutputFields

class UserApi(Resource):
    #Decorator should be inorder, Called inversely (Last element called first)
    # method_decorators = [client_validate]

    @marshal_with(OutputFields.user_fields)
    def get(self, username):
        user = user_existance_check(username)
        user.role.username = username
        return user

    @marshal_with(OutputFields.user_fields)
    def post(self, username):
        args = Parsers.password_parser.parse_args()
        user = user_existance_check(username)
        if verify_password(user.password, args["password"]):
            #Login user
            #return user object
            pass
        return {"Authentication failure": "401"}, 401

    def put(self, username):
        pass

    def delete(self, username):
        pass

    '''
    example

    /api/v1/<username>/

    GET - Get user details
    POST - Login user
    PUT - Edit user

    output :

    id : id
    username : username
    email : email
    real_name : name
    website : website
    bio : about
    created_date : created_at
    modified_date : modified_at

    role : {
            role : role,
            rol_url : url}
    votes: {
            vote : total_votes,
            question_votes : question
            answer_votes : answers
            comments_votes : comments
            }

    other details

    questions_api_url : questions
    answers_api_url : answers
    comments_api_url : comments

    '''
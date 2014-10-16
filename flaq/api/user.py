from flask.ext import restful

class User(restful.Resource):
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
    def get(self, username):
        pass

    def post(self, username):
        pass

    def put(self, username):
        pass

    def delete(self, username):
        pass
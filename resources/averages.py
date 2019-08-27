from flask_restful import Resource, reqparse
from models.averages import AverageUsernameModel


class AverageUsername(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("number", type=float, required=True)

    @staticmethod
    def get(username):
        user_average = AverageUsernameModel.find_by_username(username)
        if user_average:
            return user_average.json()["average"], 200
        return None, 404

    @staticmethod
    def put(username):
        data = AverageUsername.parser.parse_args()
        user = AverageUsernameModel.find_by_username(username)
        if user:
            user.average = (user.average * user.count + data["number"]) / (
                user.count + 1)
            user.count += 1
        else:
            user = AverageUsernameModel(username, data["number"], 1)
        user.save_to_db()
        return user.json(), 201


class GlobalAverage(Resource):
    @staticmethod
    def get():
        global_average = AverageUsernameModel.total_average()
        if global_average:
            average = next(global_average)[0]
            return {"average": average}, 200
        return None, 404

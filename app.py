from flask import Flask
from flask_restful import Api

from resources.averages import AverageUsername, GlobalAverage

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


api.add_resource(AverageUsername, '/average/<string:username>')
api.add_resource(GlobalAverage, '/average')


if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=8081, debug=True)

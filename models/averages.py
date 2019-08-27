from db import db


class AverageUsernameModel(db.Model):
    __tablename__ = 'user_averages'

    username = db.Column(db.String(100), primary_key=True)
    average = db.Column(db.Float(precision=4))
    count = db.Column(db.Integer)

    def __init__(self, username, average, count):
        self.username = username
        self.average = average
        self.count = count

    def json(self):
        return {"username": self.username, "average": self.average,
                "count": self.count}

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def total_average(cls):
        return db.engine.execute(
            "SELECT avg/cnt FROM (SELECT SUM(average*count) as avg, "
            "SUM(count) as cnt FROM user_averages)"
        )

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

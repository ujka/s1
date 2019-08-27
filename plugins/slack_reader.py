import requests
from functools import lru_cache
from rtmbot.core import Plugin, Job

SLACK_USER_INFO = "https://slack.com/api/users.info?"
AVERAGE_ENDPOINT = "http://127.0.0.1:8081/average"


class MyJob(Job):
    def __init__(self, interval):
        super().__init__(interval)
        self.last_average = None

    def run(self, slack_client):
        data = requests.get(AVERAGE_ENDPOINT).json()
        if data and self.last_average != data["average"]:
            self.last_average = data["average"]
            return [["random", f"Average for all is {data['average']}"]]


class UsersAveragePlugin(Plugin):
    def register_jobs(self):
        self.jobs.append(MyJob(10))

    def process_message(self, data):
        if data.get("type", False) == "message":
            username = self.get_username_from_id(data.get("user", None))
            if username:
                self.process_text_from_message(data, username)

    def process_text_from_message(self, data, username):
        try:
            number = float(data.get("text", "").strip())
            response = requests.put(
                f"{AVERAGE_ENDPOINT}/{username}", json={"number": number})
            average = response.json()["average"]
            self.outputs.append(
                [data['channel'], f"User {username} average is {average}"])
        except ValueError as _:
            print("User input is not a number")

    @lru_cache(maxsize=32)
    def get_username_from_id(self, user_id):
        response = requests.get(
            "%s" % SLACK_USER_INFO, {"token": self.slack_client.token,
                                     "user": user_id})
        if response.ok:
            return response.json()['user']['real_name']
        else:
            return None

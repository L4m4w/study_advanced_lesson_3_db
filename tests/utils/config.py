import os


class Server:
    def __init__(self, env):
        self.local_api = {
            "dev": os.getenv("APP_URL")
        }[env]
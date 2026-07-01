# user_api.py
class UserAPI:
    """用户模块接口封装"""

    def __init__(self, api_client):
        self.client = api_client

    def create_user(self, user_data):
        return self.client.request("POST", "/user", json=user_data)

    def get_user(self, username):
        return self.client.request("GET", f"/user/{username}")

    def delete_user(self, username):
        return self.client.request("DELETE", f"/user/{username}")
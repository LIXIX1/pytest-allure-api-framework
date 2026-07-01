
# pet_api.py
class PetAPI:
    """宠物模块接口封装"""

    def __init__(self, api_client):
        self.client = api_client

    def add_pet(self, pet_data):
        """新增宠物"""
        return self.client.request("POST", "/pet", json=pet_data)

    def get_pet(self, pet_id):
        """根据 ID 获取宠物信息"""
        return self.client.request("GET", f"/pet/{pet_id}")

    def update_pet(self, pet_data):
        """更新宠物信息"""
        return self.client.request("PUT", "/pet", json=pet_data)

    def delete_pet(self, pet_id):
        """删除宠物"""
        return self.client.request("DELETE", f"/pet/{pet_id}")
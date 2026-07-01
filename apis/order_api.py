# order_api.py
class OrderAPI:
    """订单模块接口封装"""

    def __init__(self, api_client):
        self.client = api_client

    def create_order(self, order_data):
        """创建订单"""
        return self.client.request("POST", "/store/order", json=order_data)

    def get_order(self, order_id):
        """根据 ID 获取订单信息"""
        return self.client.request("GET", f"/store/order/{order_id}")

    def delete_order(self, order_id):
        """删除订单"""
        return self.client.request("DELETE", f"/store/order/{order_id}")
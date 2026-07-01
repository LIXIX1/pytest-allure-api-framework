import pytest
import allure

from utils.allure_helper import attach_request_response
from utils.yaml_loader import YamlLoader
from apis.order_api import OrderAPI

ORDER_TEST_DATA = YamlLoader.load_data("data/order_test_data.yaml")

@allure.epic("电商核心业务")

class TestOrderBusinessFlow:

    @pytest.fixture(autouse=True)
    def setup(self, api_client):
        """每个测试用例执行前自动初始化 OrderAPI"""
        self.order_api = OrderAPI(api_client)

    @allure.title("订单模块回归: {data[case_name]} (ID: {data[payload][id]})")
    @allure.story("订单全生命周期")
    @allure.description("验证订单从创建、查询到删除的完整闭环，包含数据一致性校验。")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.parametrize(
        "data",
        ORDER_TEST_DATA,
        ids=[d["case_name"] for d in ORDER_TEST_DATA]
    )
    def test_order_full_lifecycle(self, data):
        order_data = data["payload"]
        order_id = order_data["id"]
        # ========== 步骤 1: 创建订单 ==========
        create_resp = self.order_api.create_order(order_data)
        # 使用工具函数记录请求和响应
        attach_request_response(f"1. 创建订单: {order_id}", create_resp, order_data)
        # 直接断言，失败会自动报错并停止
        assert create_resp.status_code == data["expect_code"], \
            f"创建订单失败，期望 {data['expect_code']}，实际 {create_resp.status_code}"

        # 只有创建成功，才继续后续流程
        if create_resp.status_code == 200:
            # ========== 步骤 2: 查询并验证初始状态 ==========
            get_resp = self.order_api.get_order(order_id)
            attach_request_response(f"2. 验证初始状态: {order_id}", get_resp)
            actual_status = get_resp.json().get("status")
            assert actual_status == order_data["status"], \
                f"初始状态不一致，期望: {order_data['status']}, 实际: {actual_status}"

            # ========== 步骤 3: 更新订单状态 ==========
            order_data["status"] = data["update_status"]
            update_resp = self.order_api.create_order(order_data)
            attach_request_response(f"3. 更新订单状态为: {data['update_status']}", update_resp, order_data)
            assert update_resp.status_code == 200, f"更新订单失败: {update_resp.text}"

            # ========== 步骤 4: 验证更新后的状态 ==========
            get_resp_after = self.order_api.get_order(order_id)
            attach_request_response(f"4. 验证更新后状态: {order_id}", get_resp_after)
            actual_new_status = get_resp_after.json().get("status")
            assert actual_new_status == data["update_status"], \
                f"更新后状态不一致，期望: {data['update_status']}, 实际: {actual_new_status}"

            # ========== 步骤 5: 删除订单 ==========
            del_resp = self.order_api.delete_order(order_id)
            attach_request_response(f"5. 删除订单: {order_id}", del_resp)
            assert del_resp.status_code == 200, f"删除订单失败: {del_resp.text}"

            # ========== 步骤 6: 兜底验证 ==========
            verify_resp = self.order_api.get_order(order_id)
            attach_request_response(f"6. 兜底验证: 确认订单已删除", verify_resp)
            assert verify_resp.status_code == 404, \
                f"删除后仍可查到订单(ID:{order_id})，删除操作未生效"

        # # ========== 步骤 1: 创建订单 ==========
        # with allure.step(f"1. 创建订单: {order_id}"):
        #     create_resp = self.order_api.create_order(order_data)
        #     try:
        #         assert create_resp.status_code == data["expect_code"], \
        #             f"创建订单失败，期望 {data['expect_code']}，实际 {create_resp.status_code}"
        #     except AssertionError:
        #         allure.attach(create_resp.text, name="创建失败响应", attachment_type=allure.attachment_type.TEXT)
        #         raise
        #
        # # ========== 步骤 2: 查询并验证初始状态 ==========
        # if create_resp.status_code == 200:
        #     with allure.step(f"2. 验证初始状态: {order_id}"):
        #         get_resp = self.order_api.get_order(order_id)
        #         actual_status = get_resp.json().get("status")
        #         assert actual_status == order_data["status"], \
        #             f"初始状态不一致，期望: {order_data['status']}, 实际: {actual_status}"
        #
        #     # ========== 步骤 3: 更新订单状态 ==========
        #     with allure.step(f"3. 更新订单状态为: {data['update_status']}"):
        #         order_data["status"] = data["update_status"]
        #         update_resp = self.order_api.create_order(order_data)
        #         assert update_resp.status_code == 200, f"更新订单失败: {update_resp.text}"
        #
        #     # ========== 步骤 4: 验证更新后的状态 ==========
        #     with allure.step(f"4. 验证更新后状态: {order_id}"):
        #         get_resp_after = self.order_api.get_order(order_id)
        #         actual_new_status = get_resp_after.json().get("status")
        #         assert actual_new_status == data["update_status"], \
        #             f"更新后状态不一致，期望: {data['update_status']}, 实际: {actual_new_status}"
        #
        #     # ========== 步骤 5: 删除订单 ==========
        #     with allure.step(f"5. 删除订单: {order_id}"):
        #         del_resp = self.order_api.delete_order(order_id)
        #         assert del_resp.status_code == 200, f"删除订单失败: {del_resp.text}"
        #
        #     # ========== 步骤 6: 兜底验证 ==========
        #     with allure.step(f"6. 兜底验证: 确认订单已删除"):
        #         verify_resp = self.order_api.get_order(order_id)
        #         assert verify_resp.status_code == 404, \
        #             f"删除后仍可查到订单(ID:{order_id})，删除操作未生效"
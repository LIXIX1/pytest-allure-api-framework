# testcases/test_user_flow.py
import pytest
import allure
from utils.yaml_loader import YamlLoader
from utils.allure_helper import attach_request_response  # 1. 引入工具函数
from apis.user_api import UserAPI

# 在模块级别加载数据，避免每次执行用例都读取文件
USER_TEST_DATA = YamlLoader.load_data("data/user_test_data.yaml")

@allure.feature("用户管理模块")
@allure.severity(allure.severity_level.BLOCKER)
class TestUserBusinessFlow:
    """测试用户管理的完整业务链路"""

    # 使用 autouse=True 的 Fixture 进行用例前置初始化
    @pytest.fixture(autouse=True)
    def setup(self, api_client):
        """每个用例执行前初始化 API 层"""
        self.user_api = UserAPI(api_client)

    
    @allure.story("用户增删改查全流程")
    @pytest.mark.parametrize(
        "data",
        USER_TEST_DATA,
        ids=[d["case_name"] for d in USER_TEST_DATA]  # 使用 case_name 作为用例标识
    )
    def test_user_flow(self, data):
        """
        业务链路：创建 -> 查询验证 -> 删除 -> 兜底验证
        """
        user_data = data["payload"]

        # 动态设置标题，避免 Behaviors 视图文字重叠
        allure.dynamic.title(data['case_name'])
        username = user_data["username"]

        # ========== 步骤 1: 创建用户 ==========
        create_resp = self.user_api.create_user(user_data)
        attach_request_response(f"1. 创建用户: {username}", create_resp, user_data)
        assert create_resp.status_code == data["expect_code"], \
            f"[创建失败] 状态码: {create_resp.status_code}, 响应: {create_resp.text}"

        # 只有创建成功，才继续后续流程
        if create_resp.status_code == 200:
            # ========== 步骤 2: 查询用户并验证邮箱 ==========
            get_resp = self.user_api.get_user(username)
            attach_request_response(f"2. 查询用户并验证邮箱: {username}", get_resp)
            assert get_resp.status_code == 200, f"[查询失败] 用户: {username}"
            assert get_resp.json()["email"] == user_data["email"], "邮箱数据不一致"

            # ========== 步骤 3: 删除用户 ==========
            del_resp = self.user_api.delete_user(username)
            attach_request_response(f"3. 删除用户: {username}", del_resp)
            assert del_resp.status_code == 200, f"[删除失败] 用户: {username}"

            # ========== 步骤 4: 兜底验证 ==========
            verify_resp = self.user_api.get_user(username)
            attach_request_response(f"4. 兜底验证: 确认用户已删除", verify_resp)
            # 删除后应返回 404 或 400
            assert verify_resp.status_code in [404, 400], "删除后仍可查到用户，删除失败"
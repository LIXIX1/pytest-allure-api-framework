# testcases/test_pet_flow.py
import pytest
import allure
from utils.yaml_loader import YamlLoader
from utils.allure_helper import attach_request_response  # 1. 引入工具函数
from apis.pet_api import PetAPI

# 加载宠物测试数据
PET_TEST_DATA = YamlLoader.load_data("data/pet_test_data.yaml")

@allure.feature("宠物管理模块")
class TestPetBusinessFlow:
    """测试宠物管理的完整业务链路"""

    @pytest.fixture(autouse=True)
    def setup(self, api_client):
        """每个用例执行前初始化 Pet API 层"""
        self.pet_api = PetAPI(api_client)

    @allure.title("宠物模块的回归: {data[case_name]} (ID: {data[payload][id]})")
    @allure.story("宠物增删改查全流程")
    @pytest.mark.parametrize(
        "data",
        PET_TEST_DATA,
        ids=[d["case_name"] for d in PET_TEST_DATA]
    )
    def test_pet_full_lifecycle(self, data):
        """
        业务链路：新增 -> 查询验证 -> 更新 -> 查询验证 -> 删除 -> 兜底验证
        """
        pet_data = data["payload"]
        pet_id = pet_data["id"]

        # ========== 步骤 1: 新增宠物 ==========
        add_resp = self.pet_api.add_pet(pet_data)
        attach_request_response(f"1. 新增宠物: {pet_data['name']}", add_resp, pet_data)
        assert add_resp.status_code == data["expect_code"], \
            f"[新增失败] 状态码: {add_resp.status_code}, 响应: {add_resp.text}"

        # 只有新增成功，才继续后续流程
        if add_resp.status_code == 200:
            # ========== 步骤 2: 查询并验证【新增】后的初始状态 ==========
            get_resp = self.pet_api.get_pet(pet_id)
            attach_request_response(f"2. 查询宠物并验证初始状态: {pet_id}", get_resp)
            assert get_resp.status_code == 200, f"[查询失败] 宠物ID: {pet_id}"
            assert get_resp.json()["status"] == pet_data["status"], \
                f"初始状态不一致，期望: {pet_data['status']}, 实际: {get_resp.json()['status']}"

            # ========== 步骤 3: 更新宠物状态 ==========
            pet_data["status"] = data["update_status"]
            update_resp = self.pet_api.update_pet(pet_data)
            attach_request_response(f"3. 将宠物状态更新为: {data['update_status']}", update_resp, pet_data)
            assert update_resp.status_code == 200, \
                f"[更新失败] 状态码: {update_resp.status_code}, 响应: {update_resp.text}"

            # ========== 步骤 4: 查询并验证【更新】后的最新状态 ==========
            get_resp_after_update = self.pet_api.get_pet(pet_id)
            attach_request_response(f"4. 再次查询宠物，验证更新后的状态: {pet_id}", get_resp_after_update)
            assert get_resp_after_update.status_code == 200, f"[更新后查询失败] 宠物ID: {pet_id}"
            assert get_resp_after_update.json()["status"] == data["update_status"], \
                f"更新后状态不一致，期望: {data['update_status']}, 实际: {get_resp_after_update.json()['status']}"

            # ========== 步骤 5: 删除宠物 ==========
            del_resp = self.pet_api.delete_pet(pet_id)
            attach_request_response(f"5. 删除宠物: {pet_id}", del_resp)
            assert del_resp.status_code == 200, f"[删除失败] 宠物ID: {pet_id}"

            # ========== 步骤 6: 兜底验证（删除后查询应返回 404）==========
            verify_resp = self.pet_api.get_pet(pet_id)
            attach_request_response(f"6. 兜底验证: 确认宠物已被彻底删除", verify_resp)
            assert verify_resp.status_code == 404, \
                f"删除后仍可查到宠物(ID:{pet_id})，删除操作未生效"
from pathlib import Path
import pytest
import allure

from utils.http_client import ResilientApiClient

import pytest
from utils.http_client import ResilientApiClient
from utils.yaml_loader import YamlLoader  # 假设你有这个工具类


@pytest.fixture(scope="session")
def api_client():
    """
    全局 API 客户端 Fixture
    负责初始化客户端，处理自动登录，并在测试结束后关闭连接
    """
    # 1. 读取配置
    try:
        config_data = YamlLoader.get_config()
        env_config = config_data.get("ENV_CONFIG", {}).get("test", {"BASE_URL"})

        base_url = env_config.get("BASE_URL", "https://petstore.swagger.io/v2")
        # 【关键修复】从配置中获取登录 URL 和参数
        login_url = env_config.get("LOGIN_URL", "/user/login")
        login_params = env_config.get("LOGIN_PARAMS", {"username": "test", "password": "123456"})

    except Exception as e:
        print(f"读取配置失败，使用默认值: {e}")
        base_url = "https://petstore.swagger.io/v2"
        login_url = "/user/login"
        login_params = {"username": "test", "password": "123456"}

    # 2. 实例化客户端 (补全缺失的参数)
    # 注意：这里假设你的 ResilientApiClient 设计是初始化时自动登录
    client = ResilientApiClient(
        base_url=base_url,
        login_url=login_url,  # 【补全】
        login_params=login_params  # 【补全】
    )

    yield client



# 2. 优化测试收集过程（修复中文乱码 & Allure 集成）
def pytest_collection_modifyitems(session, config, items):
    """
    在收集完测试用例后，自动根据文件名为其添加 Epic 和 Feature 标签
    """
    for item in items:
        # 1. 解决中文乱码
        item.name = item.name.encode("utf-8").decode("unicode_escape")
        item._nodeid = item._nodeid.encode("utf-8").decode("unicode_escape")

        # 2. 获取测试用例的文件名 (例如: test_pet_flow.py)
        file_name = Path(item.fspath).stem

        # 3. 定义统一的映射规则
        # 这里我们将所有用例都归为 "电商核心业务" 这个 Epic 下，避免分散
        epic_name = "电商核心业务"

        feature_name = "其他模块"  # 默认值

        if "pet" in file_name:
            feature_name = "宠物管理模块"
        elif "user" in file_name:
            feature_name = "用户管理模块"
        elif "order" in file_name:
            feature_name = "订单管理模块"

        # 4. 动态添加标签 (使用 label 方法直接覆盖或添加)
        # severity 默认为 normal
        item.add_marker(allure.severity(allure.severity_level.NORMAL))

        # 关键：添加 Epic 和 Feature
        # 注意：如果用例上已经手动写了 @allure.epic，这里的 add_marker 会追加，可能导致显示多个。
        # 建议：要么全自动化，要么全手动。这里是全自动化的写法。
        item.add_marker(allure.epic(epic_name))
        item.add_marker(allure.feature(feature_name))

        # 也可以根据文件名给个简单的描述
        item.add_marker(allure.description(f"自动化执行文件: {file_name}"))
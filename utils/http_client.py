
# http_client.py
import requests
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class ResilientApiClient:
    """带有 Token 自动刷新功能的 HTTP 客户端"""

    def __init__(self, base_url, login_url, login_params):
        self.base_url = base_url.rstrip('/')
        self.login_url = login_url
        self.login_params = login_params
        self.session = requests.Session()

        self.session.headers.update({"Content-Type": "application/json"})

        # 初始化时立即执行登录获取 Token
        self._refresh_token()
        # --- 【新增】用于 Allure 报告的数据捕获 ---
        self.last_request = None
        self.last_response = None
    def _refresh_token(self):
        """内部方法：执行登录并更新 Session Header"""
        logger.info(">>> 正在执行全局登录/Token刷新...")
        try:
            url = f"{self.base_url}{self.login_url}"
            resp = self.session.get(url, params=self.login_params, timeout=10)
            resp.raise_for_status()

            # ⚠️ 注意：根据实际 Swagger/API 返回结构调整 Key
            token = resp.json().get("message")
            if not token:
                raise ValueError("Login response missing token")

            self.session.headers.update({"Authorization": f"Bearer {token}"})
            logger.info(f">>> Token 刷新成功: {token[:10]}...")
        except Exception as e:
            logger.error(f"!!! 全局登录失败: {e}")
            raise

    def request(self, method, endpoint, **kwargs):
        """统一请求入口，包含 401 自动重试机制"""
        url = f"{self.base_url}{endpoint}"
        kwargs.setdefault("timeout", 10)

        response = self.session.request(method, url, **kwargs)

        # 核心：检测到 401 未授权，自动刷新 Token 并重试一次
        if response.status_code == 401:
            logger.warning("⚠️ 检测到 401 错误，Token 可能过期，正在自动重试...")
            self._refresh_token()
            response = self.session.request(method, url, **kwargs)

        return response
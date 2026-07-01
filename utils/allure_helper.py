# utils/allure_helper.py
import allure
import json


def attach_request_response(step_name, response, request_body=None):
    """手动将请求和响应附加到 Allure 报告中"""
    with allure.step(step_name):
        if request_body:
            req_info = f"URL: {response.request.url}\n" \
                       f"Method: {response.request.method}\n" \
                       f"Body: {json.dumps(request_body, ensure_ascii=False, indent=2)}"
            allure.attach(req_info, name="📤 请求详情", attachment_type=allure.attachment_type.TEXT)

        resp_info = f"Status Code: {response.status_code}\n" \
                    f"Body: {response.text}"
        allure.attach(resp_info, name="📥 响应详情", attachment_type=allure.attachment_type.TEXT)
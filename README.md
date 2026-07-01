#  优雅的 Pytest + Allure API 自动化测试框架

这是一个基于 Python + Pytest + Requests 构建的轻量级、高扩展性 API 自动化测试框架。它采用分层架构，支持 YAML 数据驱动，并深度定制了 Allure 报告，让接口测试既高效又具备极强的可读性。

##  核心特性

- ** 优雅的报告**：封装了 `attach_request_response` 工具函数，自动在 Allure 报告中记录请求和响应报文，告别冗长的 `try-except` 代码块。
- ** 数据驱动**：测试数据与用例逻辑完全分离，基于 YAML 管理，维护成本极低。
- ** 专业美化**：支持自定义团队 Logo、报告标题及 Environment 环境信息展示，报告“拿得出手”。
- **️ 分层架构**：API 层、工具层、用例层严格分离，易于集成 Token 刷新、数据库校验等复杂场景。
- ** 动态标题**：支持基于 YAML 数据的动态用例标题，避免 Allure Behaviors 视图文字重叠。

## ️ 快速开始

### 1. 环境准备
确保已安装 Python 3.8+。建议创建并激活虚拟环境：
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
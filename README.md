#  优雅的 Pytest + Allure API 自动化测试框架

项目简介
本项目是一个基于 Python 的轻量级接口自动化测试框架。采用 数据驱动 (Data-Driven) 的设计模式，将测试逻辑与测试数据完全分离。目前框架已覆盖 用户(User)、订单(Order) 和 宠物(Pet) 三大核心业务模块的接口测试，并集成了 Allure 生成可视化的测试报告。
️ 核心技术栈：
编程语言: Python 3.x
测试框架: Pytest (>=7.4.0)
HTTP 请求: Requests (>=2.31.0)
报告工具: Allure Pytest (>=2.13.2)
数据格式: YAML (用于管理测试数据和全局配置)
项目组织架构：
  my-api-test-framework/
├── config.yaml              # 全局配置文件
├── pytest.ini               # Pytest 运行配置
├── requirements.txt         # 依赖包清单
├── run_tests.py             # 测试运行入口
│
├── test_data/               # 📁 测试数据目录
│   ├── user_test_data.yaml
│   ├── order_test_data.yaml
│   └── pet_test_data.yaml
│
└── testcases/               # 📁 测试用例目录
    ├── test_user.py         
    ├── test_order_flow.py
    └── test_pet_flow.py

快速开始

### 1. 环境准备
确保已安装 Python 环境，克隆本项目后，在终端执行以下命令安装依赖
pip install -r requirements.txt
2. 配置环境
请修改 config.yaml 文件，填入正确的测试环境 Base URL 和测试账号信息。
3. 运行测试
方式一：使用命令行
# 运行所有模块测试
pytest

# 运行指定模块 (例如：宠物模块)
pytest test_pet.py -v -s

# 生成 Allure 结果数据
pytest --alluredir=./report_data
方式二：使用运行脚本
直接运行入口脚本启动测试并且自动生成报告
python run_tests.py
4. 查看测试报告
测试完成后，使用 Allure 生成并打开可视化报告：
allure serve ./report_data
5. 核心特性
数据驱动: 测试用例通过读取 YAML 文件自动循环执行，新增场景只需增加数据行，无需改动代码。
模块化设计: 按业务线（User/Order/Pet）独立拆分测试脚本与数据文件，结构清晰，易于扩展。
配置分离: 通过 config.yaml 统一管理多套环境配置，一键切换测试环境。
精美报告: 深度集成 Allure 报告，支持查看请求详情、响应结果及错误堆栈，方便问题排查。
6. 如何新增测试用例？
在对应的 xxx_test_data.yaml 文件中新增一组测试数据。
在对应的 test_xxx.py 文件中编写测试逻辑，读取 YAML 数据进行断言。
运行 pytest 即可自动发现并执行新用例。

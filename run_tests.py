# # run_tests.py
# import pytest
# import os
# import subprocess
# import sys
#
#
# def run():
#     print("=" * 50)
#     print("🚀 开始执行自动化测试...")
#     print("=" * 50)
#
#     # 1. 执行 Pytest
#     exit_code = pytest.main(["./testcases"])
#
#     # 2. 自动生成并打开 Allure 报告
#     if os.path.exists("./allure-results"):
#         print("\n📊 正在生成 Allure 报告...")
#         try:
#             # 调用 allure 命令行生成报告
#             subprocess.run(["allure", "generate", "./allure-results", "-o", "./allure-report", "--clean"], check=True)
#             subprocess.run(["allure", "open", "./allure-report"])
#         except FileNotFoundError:
#             print("❌ 未找到 'allure' 命令，请确保已安装 allure-commandline 并配置环境变量")
#             print("💡 提示: 可手动执行 'allure serve ./allure-results' 查看报告")
#         except Exception as e:
#             print(f"❌ 报告生成失败: {e}")
#     else:
#         print("⚠️ 未生成测试结果，请检查测试执行情况")
#
#     sys.exit(exit_code)
#
#
# if __name__ == "__main__":
#     run()
# run.py
import os
import shutil
import subprocess


def run_test():
    # 1. 清理旧的 Allure 结果目录
    results_dir = "./allure-results"
    if os.path.exists(results_dir):
        print("🧹 正在清理旧的测试报告数据...")
        shutil.rmtree(results_dir)

    # 2. 执行 Pytest 并生成 Allure 原始数据
    print("🚀 正在执行自动化测试...")
    pytest_cmd = [
        "pytest", "testcases/",
        "--alluredir", results_dir,
        "-v",
        "--clean-alluredir"
    ]
    subprocess.run(pytest_cmd)

    # 3. 启动 Allure 本地服务并自动打开浏览器
    print("📊 正在生成并打开 Allure 测试报告...")
    allure_cmd = ["allure", "serve", results_dir]
    # 修改前
    # subprocess.run(allure_cmd)

    # 修改后：添加 shell=True
    try:
        subprocess.run(allure_cmd, shell=True)
    except Exception as e:
        print(f"⚠️ 自动打开报告失败: {e}")
        print("请手动在终端运行: allure open ./allure-results")




if __name__ == "__main__":

    run_test()
import os

import pytest

if __name__ == "__main__":
    # 设置配置为test环境
    os.environ["access_token"] = "30b2cf5f-59a4-4526-8bf2-4b0439abaade"
    os.environ["PYTHONIOENCODING"] = "utf-8"
    os.environ["uc_env"] = "test"
    os.environ["base_url"] = f"https://uc-{os.environ['uc_env']}.perfect99.com/api"
    os.environ["json_url"] = "https://test-perfect-oss-uc2.oss-cn-shenzhen.aliyuncs.com"

    # 先执行测试用例，生成allure原始数据
    pytest.main(
        [
            # "-m", "test_4295",
            "--clean-alluredir",
            "-v",
            "-s",
            r"testcases\test_user_order_getStoreAgentOrderList.py",
        ]
    )

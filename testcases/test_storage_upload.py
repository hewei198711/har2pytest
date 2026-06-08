import os

import allure
from allure_commons.types import Severity

from apis.basic_services import _storage_upload


@allure.severity(Severity.CRITICAL)
@allure.feature("basic_services")
@allure.story("/storage/upload")
class TestClass:
    def setup_class(self):
        self.headers = {
            "channel": "pc",
            "client": "op",
            "content-type": "multipart/form-data",
            "authorization": f"bearer {os.environ['access_token']}",
        }

    @allure.title("TODO: 添加接口描述")
    def test_storage_upload(self):

        # 初始化测试数据字典，用于在步骤间传递数据
        test_data = {}

        @allure.step("TODO: 添加接口描述")
        def step_storage_upload():

            files = {
                "storageType": "PublicCloud",
                "clientKey": "mall-center-product",
                "file": "(binary)",
            }

            with _storage_upload(files=files, headers=self.headers) as r:
                assert r.status_code == 200
                assert r.json()["code"] == 200
                test_data["storage_upload"] = r.json()

        # 执行所有测试步骤
        step_storage_upload()

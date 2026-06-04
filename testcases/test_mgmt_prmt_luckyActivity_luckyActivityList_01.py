import os

import allure
from allure_commons.types import Severity

from apis.mall_mgmt_application import (
    _mgmt_prmt_luckyActivity_luckyActivityList,
    _mgmt_prmt_state_luckyActivity,
    _mgmt_prmt_state_waitExamineCount,
)


@allure.severity(Severity.CRITICAL)
@allure.feature("mall_mgmt_application")
@allure.story("/mgmt/prmt/luckyActivity/luckyActivityList")
class TestClass:
    def setup_class(self):
        self.headers = {
            "channel": "pc",
            "client": "op",
            "authorization": f"bearer {os.environ['access_token']}",
        }

    def test_mgmt_prmt_luckyActivity_luckyActivityList(self):

        # 初始化测试数据字典，用于在步骤间传递数据
        test_data = {}

        @allure.step("抽奖活动管理列表")
        def step_mgmt_prmt_luckyActivity_luckyActivityList():

            params = {
                "activityCode": "052202",
                "pageNum": "1",
                "pageSize": "10",
            }

            with _mgmt_prmt_luckyActivity_luckyActivityList(params=params, headers=self.headers) as r:
                assert r.status_code == 200
                assert r.json()["code"] == 200
                test_data["luckyActivity_luckyActivityList"] = r.json()

        @allure.step("抽奖活动管理各状态数量")
        def step_mgmt_prmt_state_luckyActivity():

            params = {
                "activityCode": "052202",
                "pageNum": "1",
                "pageSize": "10",
            }

            with _mgmt_prmt_state_luckyActivity(params=params, headers=self.headers) as r:
                assert r.status_code == 200
                assert r.json()["code"] == 200
                test_data["state_luckyActivity"] = r.json()

        @allure.step("待审核状态数量")
        def step_mgmt_prmt_state_waitExamineCount():

            with _mgmt_prmt_state_waitExamineCount(headers=self.headers) as r:
                assert r.status_code == 200
                assert r.json()["code"] == 200
                test_data["state_waitExamineCount"] = r.json()

        # 执行所有测试步骤
        step_mgmt_prmt_luckyActivity_luckyActivityList()
        step_mgmt_prmt_state_luckyActivity()
        step_mgmt_prmt_state_waitExamineCount()

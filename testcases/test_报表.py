import os

import allure
from allure_commons.types import Severity

from apis.mall_center_inventory import _invt_discredit_getPeriodCreditMsg
from apis.mall_store_application import (
    _appStore_store_deposit_creditCtrlLog,
    _appStore_store_deposit_details,
    _appStore_store_deposit_msg,
    _appStore_store_deposit_remitDetails,
    _appStore_store_getManageWordContent,
    _appStore_store_getSignBankAccountList,
)
from apis.settle_job import _months_deposit_billCheck_page


@allure.severity(Severity.CRITICAL)
@allure.epic("建议输入被测接口所属的微服务，如 mall_store_application")
@allure.feature("建议输入被测业务功能模块，如 订单管理")
@allure.story("建议输入被测接口，如 /appStore/order/orderSign/signCommit")
@allure.title("建议输入测试用例名称，如 提交订单")
def test_har_api_flow():

    # 初始化测试数据字典，用于在步骤间传递数据
    test_data = {
        "headers": {
            "channel": "pc",
            "client": "op",
            "content-type": "application/json;charset=UTF-8",
            "authorization": f"bearer {os.environ['access_token']}",
        },
    }

    @allure.step("获取进行中的分期信用额设置")
    def step_invt_discredit_getPeriodCreditMsg():

        params = {"storeCode": "914008"}
        with _invt_discredit_getPeriodCreditMsg(params=params, headers=test_data["headers"]) as r:
            assert r.status_code == 200
            assert r.json()["code"] == 200
            test_data["discredit_getPeriodCreditMsg"] = r.json()

    @allure.step("85%信誉额调整历史")
    def step_appStore_store_deposit_creditCtrlLog():

        data = {"storeCode": "914008", "pageNum": 1, "pageSize": 20}
        with _appStore_store_deposit_creditCtrlLog(data=data, headers=test_data["headers"]) as r:
            assert r.status_code == 200
            assert r.json()["code"] == 200
            test_data["deposit_creditCtrlLog"] = r.json()

    @allure.step("获取服务中心提示语内容")
    def step_appStore_store_getManageWordContent():

        params = {"type": "2"}
        with _appStore_store_getManageWordContent(params=params, headers=test_data["headers"]) as r:
            assert r.status_code == 200
            assert r.json()["code"] == 200
            test_data["store_getManageWordContent"] = r.json()

    @allure.step("获取签约银行列表")
    def step_appStore_store_getSignBankAccountList():

        with _appStore_store_getSignBankAccountList(headers=test_data["headers"]) as r:
            assert r.status_code == 200
            assert r.json()["code"] == 200
            test_data["store_getSignBankAccountList"] = r.json()

    @allure.step("获取服务中心可用押货保证金余额")
    def step_appStore_store_deposit_msg():

        params = {"storeCode": "914008"}
        with _appStore_store_deposit_msg(params=params, headers=test_data["headers"]) as r:
            assert r.status_code == 200
            assert r.json()["code"] == 200
            test_data["deposit_msg"] = r.json()

    @allure.step("获取服务中心可用押货保证金余额")
    def step_1_appStore_store_deposit_msg():

        params = {"storeCode": "914008", "month": "2026-04"}
        with _appStore_store_deposit_msg(params=params, headers=test_data["headers"]) as r:
            assert r.status_code == 200
            assert r.json()["code"] == 200
            test_data["deposit_msg"] = r.json()

    @allure.step("获取服务中心可用押货保证金余额")
    def step_2_appStore_store_deposit_msg():

        params = {"month": "2026-04", "storeCode": "914008"}
        with _appStore_store_deposit_msg(params=params, headers=test_data["headers"]) as r:
            assert r.status_code == 200
            assert r.json()["code"] == 200
            test_data["deposit_msg"] = r.json()

    @allure.step("获取服务中心押货保证金增减明细")
    def step_appStore_store_deposit_details():

        data = {
            "mortgageOrderNoOrBusinessNo": "",
            "endMonth": "202604",
            "pageNum": 1,
            "pageSize": 20,
            "startMonth": "202604",
            "storeCode": "914008",
        }
        with _appStore_store_deposit_details(data=data, headers=test_data["headers"]) as r:
            assert r.status_code == 200
            assert r.json()["code"] == 200
            test_data["deposit_details"] = r.json()

    @allure.step("85折押货保证金对账单分页列表")
    def step_months_deposit_billCheck_page():

        data = {"pageNum": 1, "pageSize": 20, "storeCode": "914008", "startMonth": "202604", "endMonth": "202604"}
        with _months_deposit_billCheck_page(data=data, headers=test_data["headers"]) as r:
            assert r.status_code == 200
            assert r.json()["code"] == 200
            test_data["billCheck_page"] = r.json()

    @allure.step("获取服务中心押货保证金汇退明细")
    def step_appStore_store_deposit_remitDetails():

        data = {"pageNum": 1, "pageSize": 20, "storeCode": "914008"}
        with _appStore_store_deposit_remitDetails(data=data, headers=test_data["headers"]) as r:
            assert r.status_code == 200
            assert r.json()["code"] == 200
            test_data["deposit_remitDetails"] = r.json()

    # 执行所有测试步骤
    step_invt_discredit_getPeriodCreditMsg()
    step_appStore_store_deposit_creditCtrlLog()
    step_appStore_store_getManageWordContent()
    step_appStore_store_getSignBankAccountList()
    step_appStore_store_deposit_msg()
    step_1_appStore_store_deposit_msg()
    step_2_appStore_store_deposit_msg()
    step_appStore_store_deposit_details()
    step_months_deposit_billCheck_page()
    step_appStore_store_deposit_remitDetails()

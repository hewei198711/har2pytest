import os

import allure
from allure_commons.types import Severity

from apis.mall_center_user import (
    _user_mgmt_order_detail,
    _user_mgmt_order_return_queryOrder,
    _user_mgmt_order_return_submit,
)


@allure.severity(Severity.CRITICAL)
@allure.epic("mall_center_user")
@allure.feature("建议输入被测业务功能模块，如 订单管理")
@allure.story("/user/mgmt/order/return/submit")
@allure.title("提交售后")
def test_user_mgmt_order_return_submit():

    # 初始化测试数据字典，用于在步骤间传递数据
    test_data = {
        "headers": {
            "channel": "pc",
            "client": "op",
            "content-type": "application/json;charset=UTF-8",
            "authorization": f"bearer {os.environ['access_token']}",
        },
    }

    @allure.step("分页查询代客售后订单管理列表")
    def step_user_mgmt_order_return_queryOrder():

        data = {
            "orderNo": None,
            "customerPhone": None,
            "customerCard": None,
            "creatorCard": None,
            "exchangeNoWord": None,
            "customerType": None,
            "expressType": None,
            "orderWay": None,
            "customerSource": None,
            "exchangeTimeBegin": None,
            "exchangeTimeEnd": None,
            "pageNum": 1,
            "pageSize": 10,
        }
        with _user_mgmt_order_return_queryOrder(data=data, headers=test_data["headers"]) as r:
            assert r.status_code == 200
            assert r.json()["code"] == 200
            test_data["return_queryOrder"] = r.json()

    @allure.step("订单详情")
    def step_user_mgmt_order_detail():

        params = {"orderNo": "EX002000260416000003"}
        with _user_mgmt_order_detail(params=params, headers=test_data["headers"]) as r:
            assert r.status_code == 200
            assert r.json()["code"] == 200
            test_data["order_detail"] = r.json()

    @allure.step("订单详情")
    def step_1_user_mgmt_order_detail():

        params = {"orderNo": "EX002000260416000003"}
        with _user_mgmt_order_detail(params=params, headers=test_data["headers"]) as r:
            assert r.status_code == 200
            assert r.json()["code"] == 200
            test_data["order_detail"] = r.json()

    @allure.step("提交售后")
    def step_user_mgmt_order_return_submit():

        data = {"orderNo": "EX002000260416000003", "returnReason": "111111111111111111111111111111111"}
        with _user_mgmt_order_return_submit(data=data, headers=test_data["headers"]) as r:
            assert r.status_code == 200
            assert r.json()["code"] == 200
            test_data["return_submit"] = r.json()

    @allure.step("订单详情")
    def step_2_user_mgmt_order_detail():

        params = {"orderNo": "EX002000260416000003"}
        with _user_mgmt_order_detail(params=params, headers=test_data["headers"]) as r:
            assert r.status_code == 200
            assert r.json()["code"] == 200
            test_data["order_detail"] = r.json()

    @allure.step("分页查询代客售后订单管理列表")
    def step_1_user_mgmt_order_return_queryOrder():

        data = {
            "orderNo": None,
            "customerPhone": None,
            "customerCard": None,
            "creatorCard": None,
            "exchangeNoWord": None,
            "customerType": None,
            "expressType": None,
            "orderWay": None,
            "customerSource": None,
            "exchangeTimeBegin": None,
            "exchangeTimeEnd": None,
            "pageNum": 1,
            "pageSize": 10,
        }
        with _user_mgmt_order_return_queryOrder(data=data, headers=test_data["headers"]) as r:
            assert r.status_code == 200
            assert r.json()["code"] == 200
            test_data["return_queryOrder"] = r.json()

    # 执行所有测试步骤
    step_user_mgmt_order_return_queryOrder()
    step_user_mgmt_order_detail()
    step_1_user_mgmt_order_detail()
    step_user_mgmt_order_return_submit()
    step_2_user_mgmt_order_detail()
    step_1_user_mgmt_order_return_queryOrder()

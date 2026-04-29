import os

import allure
from setting import P1

from apis.mall_center_user import (
    _user_mgmt_order_detail,
    _user_mgmt_order_return_queryOrder,
    _user_mgmt_order_return_submit,
)


@allure.severity(P1)
@allure.feature("请填写被测试接口所属的微服务名称，如 mall_store_application")
@allure.story("请填写被测试接口，如 /appStore/order/orderSign/signCommit")
@allure.title("请填写测试用例名称，如 签约购提交订单")
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

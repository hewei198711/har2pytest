import os

import allure
from allure_commons.types import Severity

from apis.mall_store_application import (
    _appStore_common_isStoreInTrafficControl,
    _appStore_store_dis_mortgageOrder_detail_id,
    _appStore_store_dis_mortgageOrder_getMortgageAmount,
)


@allure.severity(Severity.CRITICAL)
@allure.feature("mall_store_application")
@allure.story("/appStore/store/dis/mortgageOrder/detail/{id}")
@allure.title("押货单详情")
def test_appStore_store_dis_mortgageOrder_detail_id():

    # 初始化测试数据字典，用于在步骤间传递数据
    test_data = {
        "headers": {
            "channel": "pc",
            "client": "op",
            "content-type": "application/json;charset=UTF-8",
            "authorization": f"bearer {os.environ['access_token']}",
        },
    }

    @allure.step("押货单详情")
    def step_appStore_store_dis_mortgageOrder_detail_id():

        params = {"id": "96453"}
        with _appStore_store_dis_mortgageOrder_detail_id(params=params, headers=test_data["headers"]) as r:
            assert r.status_code == 200
            assert r.json()["code"] == 200
            test_data["detail_id"] = r.json()

    @allure.step("查询店铺押货余额与限额")
    def step_appStore_store_dis_mortgageOrder_getMortgageAmount():

        with _appStore_store_dis_mortgageOrder_getMortgageAmount(headers=test_data["headers"]) as r:
            assert r.status_code == 200
            assert r.json()["code"] == 200
            test_data["mortgageOrder_getMortgageAmount"] = r.json()

    @allure.step("店铺是否处于交通管控")
    def step_appStore_common_isStoreInTrafficControl():

        with _appStore_common_isStoreInTrafficControl(headers=test_data["headers"]) as r:
            assert r.status_code == 200
            assert r.json()["code"] == 200
            test_data["common_isStoreInTrafficControl"] = r.json()

    # 执行所有测试步骤
    step_appStore_store_dis_mortgageOrder_detail_id()
    step_appStore_store_dis_mortgageOrder_getMortgageAmount()
    step_appStore_common_isStoreInTrafficControl()

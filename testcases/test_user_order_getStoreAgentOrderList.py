import os

import allure
import pytest
from allure_commons.types import Severity

from apis.mall_center_user import _user_order_getStoreAgentOrderList


@allure.severity(Severity.NORMAL)
@allure.feature("mall_center_user")
@allure.story("/user/order/getStoreAgentOrderList")
class TestClass:
    def setup_class(self):
        self.headers = {
            "channel": "pc",
            "client": "op",
            "authorization": f"bearer {os.environ['access_token']}",
        }

    @pytest.mark.parametrize("orderNo", ["EX914008260409000002"])
    @allure.title("PC店铺查询兑换订单列表: 兑换流水号 查询")
    def test_0_user_order_getStoreAgentOrderList(self, orderNo):

        params = {
            "orderNo": orderNo,
            "exchangeType": None,
            "customerPhone": None,
            "customerCard": None,
            "customerName": None,
            "batchOrderNo": None,
            "creatorCard": None,
            "orderStatus": None,
            "pageNum": 1,
            "pageSize": 10,
            "hxTimeBegin": None,
            "hxTimeEnd": None,
            "exchangeTimeBegin": None,
            "exchangeTimeEnd": None,
        }
        with _user_order_getStoreAgentOrderList(data=params, headers=self.headers) as r:
            assert r.status_code == 200
            assert r.json()["code"] == 200

    @pytest.mark.parametrize("exchangeType", [1, 2, 3])
    @allure.title("PC店铺查询兑换订单列表: 兑换产品类型 查询")
    def test_1_user_order_getStoreAgentOrderList(self, exchangeType):

        params = {
            "exchangeType": exchangeType,
            "orderNo": "",
            "customerPhone": None,
            "customerCard": None,
            "customerName": None,
            "batchOrderNo": None,
            "creatorCard": None,
            "orderStatus": None,
            "pageNum": 1,
            "pageSize": 10,
            "hxTimeBegin": None,
            "hxTimeEnd": None,
            "exchangeTimeBegin": None,
            "exchangeTimeEnd": None,
        }
        with _user_order_getStoreAgentOrderList(data=params, headers=self.headers) as r:
            assert r.status_code == 200
            assert r.json()["code"] == 200

    @pytest.mark.parametrize("hxTimeBegin,hxTimeEnd", [("2026-03-01", "2026-03-31")])
    @allure.title("PC店铺查询兑换订单列表: 核销时间-核销时间 查询")
    def test_2_user_order_getStoreAgentOrderList(self, hxTimeBegin, hxTimeEnd):

        params = {
            "hxTimeBegin": hxTimeBegin,
            "hxTimeEnd": hxTimeEnd,
            "orderNo": "",
            "exchangeType": "",
            "customerPhone": None,
            "customerCard": None,
            "customerName": None,
            "batchOrderNo": None,
            "creatorCard": None,
            "orderStatus": None,
            "pageNum": 1,
            "pageSize": 10,
            "exchangeTimeBegin": None,
            "exchangeTimeEnd": None,
        }
        with _user_order_getStoreAgentOrderList(data=params, headers=self.headers) as r:
            assert r.status_code == 200
            assert r.json()["code"] == 200

    @pytest.mark.parametrize("customerPhone", ["15876402008"])
    @allure.title("PC店铺查询兑换订单列表: 顾客手机号 查询")
    def test_3_user_order_getStoreAgentOrderList(self, customerPhone):

        params = {
            "customerPhone": customerPhone,
            "orderNo": "",
            "exchangeType": "",
            "writeoffTime": None,
            "customerCard": None,
            "customerName": None,
            "batchOrderNo": None,
            "creatorCard": None,
            "orderStatus": None,
            "pageNum": 1,
            "pageSize": 10,
            "exchangeTimeBegin": None,
            "exchangeTimeEnd": None,
        }
        with _user_order_getStoreAgentOrderList(data=params, headers=self.headers) as r:
            assert r.status_code == 200
            assert r.json()["code"] == 200

    @pytest.mark.parametrize("customerCard", ["3000004669"])
    @allure.title("PC店铺查询兑换订单列表: 顾客卡号 查询")
    def test_4_user_order_getStoreAgentOrderList(self, customerCard):

        params = {
            "customerCard": customerCard,
            "orderNo": "",
            "exchangeType": "",
            "writeoffTime": None,
            "customerPhone": "",
            "customerName": None,
            "batchOrderNo": None,
            "creatorCard": None,
            "orderStatus": None,
            "pageNum": 1,
            "pageSize": 10,
            "exchangeTimeBegin": None,
            "exchangeTimeEnd": None,
        }
        with _user_order_getStoreAgentOrderList(data=params, headers=self.headers) as r:
            assert r.status_code == 200
            assert r.json()["code"] == 200

    @pytest.mark.parametrize("customerName", ["李卡卡"])
    @allure.title("PC店铺查询兑换订单列表: 顾客姓名 查询")
    def test_5_user_order_getStoreAgentOrderList(self, customerName):

        params = {
            "customerName": customerName,
            "orderNo": "",
            "exchangeType": "",
            "writeoffTime": None,
            "customerPhone": "",
            "customerCard": "",
            "batchOrderNo": None,
            "creatorCard": None,
            "orderStatus": None,
            "pageNum": 1,
            "pageSize": 10,
            "exchangeTimeBegin": None,
            "exchangeTimeEnd": None,
        }
        with _user_order_getStoreAgentOrderList(data=params, headers=self.headers) as r:
            assert r.status_code == 200
            assert r.json()["code"] == 200

    @pytest.mark.parametrize("batchOrderNo", ["EXHZ9140082603000001"])
    @allure.title("PC店铺查询兑换订单列表: 批量兑换单号 查询")
    def test_6_user_order_getStoreAgentOrderList(self, batchOrderNo):

        params = {
            "batchOrderNo": batchOrderNo,
            "orderNo": "",
            "exchangeType": "",
            "writeoffTime": None,
            "customerPhone": "",
            "customerCard": "",
            "customerName": "",
            "creatorCard": None,
            "orderStatus": None,
            "pageNum": 1,
            "pageSize": 10,
            "exchangeTimeBegin": None,
            "exchangeTimeEnd": None,
        }
        with _user_order_getStoreAgentOrderList(data=params, headers=self.headers) as r:
            assert r.status_code == 200
            assert r.json()["code"] == 200

    @pytest.mark.parametrize("exchangeTimeBegin,exchangeTimeEnd", [("2026-03-01", "2026-03-31")])
    @allure.title("PC店铺查询兑换订单列表: 兑换时间-兑换时间 查询")
    def test_7_user_order_getStoreAgentOrderList(self, exchangeTimeBegin, exchangeTimeEnd):

        params = {
            "exchangeTimeBegin": exchangeTimeBegin,
            "exchangeTimeEnd": exchangeTimeEnd,
            "orderNo": "",
            "exchangeType": "",
            "writeoffTime": None,
            "customerPhone": "",
            "customerCard": "",
            "customerName": "",
            "batchOrderNo": "",
            "creatorCard": None,
            "orderStatus": None,
            "pageNum": 1,
            "pageSize": 10,
        }
        with _user_order_getStoreAgentOrderList(data=params, headers=self.headers) as r:
            assert r.status_code == 200
            assert r.json()["code"] == 200

    @pytest.mark.parametrize("creatorCard", ["00064658"])
    @allure.title("PC店铺查询兑换订单列表: 开单人卡号 查询")
    def test_8_user_order_getStoreAgentOrderList(self, creatorCard):

        params = {
            "creatorCard": creatorCard,
            "orderNo": "",
            "exchangeType": "",
            "writeoffTime": None,
            "customerPhone": "",
            "customerCard": "",
            "customerName": "",
            "batchOrderNo": "",
            "exchangeTime": None,
            "orderStatus": None,
            "pageNum": 1,
            "pageSize": 10,
        }
        with _user_order_getStoreAgentOrderList(data=params, headers=self.headers) as r:
            assert r.status_code == 200
            assert r.json()["code"] == 200

    @pytest.mark.parametrize(
        "creatorCard,orderStatus", [("00064658", 2), ("00064658", 6), ("00064658", 99), ("00064658", 5)]
    )
    @allure.title("PC店铺查询兑换订单列表: 开单人卡号-订单状态 1 查询")
    def test_9_user_order_getStoreAgentOrderList(self, creatorCard, orderStatus):

        params = {
            "creatorCard": creatorCard,
            "orderStatus": orderStatus,
            "orderNo": "",
            "exchangeType": "",
            "writeoffTime": None,
            "customerPhone": "",
            "customerCard": "",
            "customerName": "",
            "batchOrderNo": "",
            "exchangeTime": None,
            "pageNum": 1,
            "pageSize": 10,
        }
        with _user_order_getStoreAgentOrderList(data=params, headers=self.headers) as r:
            assert r.status_code == 200
            assert r.json()["code"] == 200

    @pytest.mark.parametrize("orderStatus", [99, 5])
    @allure.title("PC店铺查询兑换订单列表: 订单状态 查询")
    def test_10_user_order_getStoreAgentOrderList(self, orderStatus):

        params = {
            "orderStatus": orderStatus,
            "orderNo": "",
            "exchangeType": "",
            "writeoffTime": None,
            "customerPhone": "",
            "customerCard": "",
            "customerName": "",
            "batchOrderNo": "",
            "exchangeTime": None,
            "creatorCard": "",
            "pageNum": 1,
            "pageSize": 10,
        }
        with _user_order_getStoreAgentOrderList(data=params, headers=self.headers) as r:
            assert r.status_code == 200
            assert r.json()["code"] == 200

import os

import allure
import pytest
from allure_commons.types import Severity

from apis.mall_center_user import _user_order_getStoreAgentOrderList


@allure.feature("mall_center_user")
@allure.story("/user/order/getStoreAgentOrderList")
@allure.description("""接口说明：
- 接口名称：PC店铺查询兑换订单列表
- 接口地址：/user/order/getStoreAgentOrderList

主要参数说明：
- exchangeTimeEnd：兑换时间-结束
- exchangeType：兑换产品类型 1-优惠券,2-实物物品,3-油葱学堂课程,4-会议室,5体验中心兑换品
- pageSize：# TODO 请填写参数备注
- hxTimeEnd：核销时间-结束
- batchOrderNo：批量兑换单号
- customerCard：顾客卡号
- hxTimeBegin：核销时间-开始
- exchangeTimeBegin：兑换时间-开始
- customerPhone：顾客手机号
- creatorCard：开单人卡号
- orderStatus：订单状态 1->待支付 2->待发货 3->待收货(已发货) 4->已取消 5->已退货 6->待核销 99->已完成
- pageNum：# TODO 请填写参数备注
- orderNo：兑换流水号
- customerName：顾客姓名
""")
class TestClass:
    # 初始化测试数据字典，用于在步骤间传递数据
    def setup_class(self):
        self.headers = {
            "channel": "pc",
            "client": "op",
            "content-type": "application/json;charset=UTF-8",
            "authorization": f"bearer {os.environ['access_token']}",
        }

    @pytest.mark.test_4291
    @pytest.mark.parametrize("orderNo, p", [("EX914008260409000002", Severity.NORMAL)])
    @allure.title("PC店铺查询兑换订单列表-成功路径: 兑换流水号 查询")
    def test_0_user_order_getStoreAgentOrderList(self, orderNo, p):

        # 用例级别
        allure.dynamic.severity(p)

        data = {
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
        with _user_order_getStoreAgentOrderList(data=data, headers=self.headers) as r:
            assert r.status_code == 200
            assert r.json()["code"] == 200
            data_list = r.json()["data"]["list"]
            assert len(data_list) > 0, "返回数据列表为空"
            if any(i.get("orderNo") is not None for i in data_list):
                assert any(i.get("orderNo") == orderNo for i in data_list)

    @pytest.mark.test_4291
    @pytest.mark.parametrize("exchangeType, p", [(1, Severity.NORMAL), (2, Severity.NORMAL), (3, Severity.NORMAL)])
    @allure.title("PC店铺查询兑换订单列表-成功路径: 兑换产品类型 查询")
    def test_1_user_order_getStoreAgentOrderList(self, exchangeType, p):

        # 用例级别
        allure.dynamic.severity(p)

        data = {
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
        with _user_order_getStoreAgentOrderList(data=data, headers=self.headers) as r:
            assert r.status_code == 200
            assert r.json()["code"] == 200
            data_list = r.json()["data"]["list"]
            assert len(data_list) > 0, "返回数据列表为空"
            if any(i.get("exchangeType") is not None for i in data_list):
                assert any(i.get("exchangeType") == exchangeType for i in data_list)

    @pytest.mark.test_4291
    @pytest.mark.parametrize("hxTimeBegin, hxTimeEnd, p", [("2026-03-01", "2026-03-31", Severity.NORMAL)])
    @allure.title("PC店铺查询兑换订单列表-成功路径: 核销时间 查询")
    def test_2_user_order_getStoreAgentOrderList(self, hxTimeBegin, hxTimeEnd, p):

        # 用例级别
        allure.dynamic.severity(p)

        data = {
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
        with _user_order_getStoreAgentOrderList(data=data, headers=self.headers) as r:
            assert r.status_code == 200
            assert r.json()["code"] == 200
            data_list = r.json()["data"]["list"]
            assert len(data_list) > 0, "返回数据列表为空"

    @pytest.mark.test_4291
    @pytest.mark.parametrize("customerPhone, p", [("15876402008", Severity.NORMAL)])
    @allure.title("PC店铺查询兑换订单列表-成功路径: 顾客手机号 查询")
    def test_3_user_order_getStoreAgentOrderList(self, customerPhone, p):

        # 用例级别
        allure.dynamic.severity(p)

        data = {
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
        with _user_order_getStoreAgentOrderList(data=data, headers=self.headers) as r:
            assert r.status_code == 200
            assert r.json()["code"] == 200
            data_list = r.json()["data"]["list"]
            assert len(data_list) > 0, "返回数据列表为空"
            if any(i.get("customerPhone") is not None for i in data_list):
                assert any(i.get("customerPhone") == customerPhone for i in data_list)

    @pytest.mark.test_4291
    @pytest.mark.parametrize("customerCard, p", [("3000004669", Severity.NORMAL)])
    @allure.title("PC店铺查询兑换订单列表-成功路径: 顾客卡号 查询")
    def test_4_user_order_getStoreAgentOrderList(self, customerCard, p):

        # 用例级别
        allure.dynamic.severity(p)

        data = {
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
        with _user_order_getStoreAgentOrderList(data=data, headers=self.headers) as r:
            assert r.status_code == 200
            assert r.json()["code"] == 200
            data_list = r.json()["data"]["list"]
            assert len(data_list) > 0, "返回数据列表为空"
            if any(i.get("customerCard") is not None for i in data_list):
                assert any(i.get("customerCard") == customerCard for i in data_list)

    @pytest.mark.test_4291
    @pytest.mark.parametrize("customerName, p", [("李卡卡", Severity.NORMAL)])
    @allure.title("PC店铺查询兑换订单列表-成功路径: 顾客姓名 查询")
    def test_5_user_order_getStoreAgentOrderList(self, customerName, p):

        # 用例级别
        allure.dynamic.severity(p)

        data = {
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
        with _user_order_getStoreAgentOrderList(data=data, headers=self.headers) as r:
            assert r.status_code == 200
            assert r.json()["code"] == 200
            data_list = r.json()["data"]["list"]
            assert len(data_list) > 0, "返回数据列表为空"
            if any(i.get("customerName") is not None for i in data_list):
                assert any(i.get("customerName") == customerName for i in data_list)

    @pytest.mark.test_4291
    @pytest.mark.parametrize("batchOrderNo, p", [("EXHZ9140082603000001", Severity.NORMAL)])
    @allure.title("PC店铺查询兑换订单列表-成功路径: 批量兑换单号 查询")
    def test_6_user_order_getStoreAgentOrderList(self, batchOrderNo, p):

        # 用例级别
        allure.dynamic.severity(p)

        data = {
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
        with _user_order_getStoreAgentOrderList(data=data, headers=self.headers) as r:
            assert r.status_code == 200
            assert r.json()["code"] == 200
            data_list = r.json()["data"]["list"]
            assert len(data_list) > 0, "返回数据列表为空"
            if any(i.get("batchOrderNo") is not None for i in data_list):
                assert any(i.get("batchOrderNo") == batchOrderNo for i in data_list)

    @pytest.mark.test_4291
    @pytest.mark.parametrize("exchangeTimeBegin, exchangeTimeEnd, p", [("2026-03-01", "2026-03-31", Severity.NORMAL)])
    @allure.title("PC店铺查询兑换订单列表-成功路径: 兑换时间 查询")
    def test_7_user_order_getStoreAgentOrderList(self, exchangeTimeBegin, exchangeTimeEnd, p):

        # 用例级别
        allure.dynamic.severity(p)

        data = {
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
        with _user_order_getStoreAgentOrderList(data=data, headers=self.headers) as r:
            assert r.status_code == 200
            assert r.json()["code"] == 200
            data_list = r.json()["data"]["list"]
            assert len(data_list) > 0, "返回数据列表为空"

    @pytest.mark.test_4291
    @pytest.mark.parametrize("creatorCard, p", [("00064658", Severity.NORMAL)])
    @allure.title("PC店铺查询兑换订单列表-成功路径: 开单人卡号 查询")
    def test_8_user_order_getStoreAgentOrderList(self, creatorCard, p):

        # 用例级别
        allure.dynamic.severity(p)

        data = {
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
        with _user_order_getStoreAgentOrderList(data=data, headers=self.headers) as r:
            assert r.status_code == 200
            assert r.json()["code"] == 200
            data_list = r.json()["data"]["list"]
            assert len(data_list) > 0, "返回数据列表为空"
            if any(i.get("creatorCard") is not None for i in data_list):
                assert any(i.get("creatorCard") == creatorCard for i in data_list)

    @pytest.mark.test_4291
    @pytest.mark.parametrize(
        "creatorCard, orderStatus, p",
        [
            ("00064658", 2, Severity.NORMAL),
            ("00064658", 6, Severity.NORMAL),
            ("00064658", 99, Severity.NORMAL),
            ("00064658", 5, Severity.NORMAL),
        ],
    )
    @allure.title("PC店铺查询兑换订单列表-成功路径: 开单人卡号-订单状态 1 查询")
    def test_9_user_order_getStoreAgentOrderList(self, creatorCard, orderStatus, p):

        # 用例级别
        allure.dynamic.severity(p)

        data = {
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
        with _user_order_getStoreAgentOrderList(data=data, headers=self.headers) as r:
            assert r.status_code == 200
            assert r.json()["code"] == 200
            data_list = r.json()["data"]["list"]
            assert len(data_list) > 0, "返回数据列表为空"

    @pytest.mark.test_4291
    @pytest.mark.parametrize("orderStatus, p", [(99, Severity.NORMAL), (5, Severity.NORMAL)])
    @allure.title("PC店铺查询兑换订单列表-成功路径: 订单状态 查询")
    def test_10_user_order_getStoreAgentOrderList(self, orderStatus, p):

        # 用例级别
        allure.dynamic.severity(p)

        data = {
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
        with _user_order_getStoreAgentOrderList(data=data, headers=self.headers) as r:
            assert r.status_code == 200
            assert r.json()["code"] == 200
            data_list = r.json()["data"]["list"]
            assert len(data_list) > 0, "返回数据列表为空"
            if any(i.get("orderStatus") is not None for i in data_list):
                assert any(i.get("orderStatus") == orderStatus for i in data_list)

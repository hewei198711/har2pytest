import os

import allure
import pytest
from allure_commons.types import Severity

from apis.mall_center_user import _user_mgmt_order_return_queryOrder


@allure.feature("mall_center_user")
@allure.story("/user/mgmt/order/return/queryOrder")
@allure.description("""接口说明：
- 接口名称：分页查询代客售后订单管理列表
- 接口地址：/user/mgmt/order/return/queryOrder

主要参数说明：
- creatorCard：开单人卡号
- customerSource：顾客来源平台:0->商城mall；1->健康health；2->学堂edu；4->荟友趣
- exchangeTimeEnd：兑换时间-结束
- customerCard：顾客卡号
- orderNo：兑换流水号
- exchangeNoWord：兑换品编码/名称
- pageSize：# TODO 请填写参数备注
- customerPhone：顾客手机号
- pageNum：# TODO 请填写参数备注
- customerType：顾客类型 1->普通顾客 2->优惠顾客 3->云商 4->微店 5->云+子账号
- expressType：配送方式 1->服务中心自提 2->公司配送
- exchangeTimeBegin：兑换时间-开始
- orderWay：下单方式 1->自购订单 2->代购订单
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

    @pytest.mark.parametrize("orderNo, p", [("EX914008260407000001", Severity.NORMAL)])
    @allure.title("分页查询代客售后订单管理列表-成功路径: 兑换流水号 查询")
    def test_0_user_mgmt_order_return_queryOrder(self, orderNo, p):

        # 用例级别
        allure.dynamic.severity(p)

        data = {
            "orderNo": orderNo,
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
        with _user_mgmt_order_return_queryOrder(data=data, headers=self.headers) as r:
            assert r.status_code == 200
            assert r.json()["code"] == 200
            data_list = r.json()["data"]["list"]
            assert len(data_list) > 0, "返回数据列表为空"
            if any(i.get("orderNo") is not None for i in data_list):
                assert any(i.get("orderNo") == orderNo for i in data_list)

    @pytest.mark.parametrize("customerPhone, p", [("15876402008", Severity.NORMAL)])
    @allure.title("分页查询代客售后订单管理列表-成功路径: 顾客手机号 查询")
    def test_1_user_mgmt_order_return_queryOrder(self, customerPhone, p):

        # 用例级别
        allure.dynamic.severity(p)

        data = {
            "customerPhone": customerPhone,
            "orderNo": "",
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
        with _user_mgmt_order_return_queryOrder(data=data, headers=self.headers) as r:
            assert r.status_code == 200
            assert r.json()["code"] == 200
            data_list = r.json()["data"]["list"]
            assert len(data_list) > 0, "返回数据列表为空"
            if any(i.get("customerPhone") is not None for i in data_list):
                assert any(i.get("customerPhone") == customerPhone for i in data_list)

    @pytest.mark.parametrize("customerCard, p", [("3000004669", Severity.NORMAL)])
    @allure.title("分页查询代客售后订单管理列表-成功路径: 顾客卡号 查询")
    def test_2_user_mgmt_order_return_queryOrder(self, customerCard, p):

        # 用例级别
        allure.dynamic.severity(p)

        data = {
            "customerCard": customerCard,
            "orderNo": "",
            "customerPhone": "",
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
        with _user_mgmt_order_return_queryOrder(data=data, headers=self.headers) as r:
            assert r.status_code == 200
            assert r.json()["code"] == 200
            data_list = r.json()["data"]["list"]
            assert len(data_list) > 0, "返回数据列表为空"
            if any(i.get("customerCard") is not None for i in data_list):
                assert any(i.get("customerCard") == customerCard for i in data_list)

    @pytest.mark.parametrize("creatorCard, p", [("00064658", Severity.NORMAL)])
    @allure.title("分页查询代客售后订单管理列表-成功路径: 开单人卡号 查询")
    def test_3_user_mgmt_order_return_queryOrder(self, creatorCard, p):

        # 用例级别
        allure.dynamic.severity(p)

        data = {
            "creatorCard": creatorCard,
            "orderNo": "",
            "customerPhone": "",
            "customerCard": "",
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
        with _user_mgmt_order_return_queryOrder(data=data, headers=self.headers) as r:
            assert r.status_code == 200
            assert r.json()["code"] == 200
            data_list = r.json()["data"]["list"]
            assert len(data_list) > 0, "返回数据列表为空"
            if any(i.get("creatorCard") is not None for i in data_list):
                assert any(i.get("creatorCard") == creatorCard for i in data_list)

    @pytest.mark.parametrize("exchangeNoWord, p", [("TYLJD003", Severity.NORMAL), ("TYL金豆003实物", Severity.NORMAL)])
    @allure.title("分页查询代客售后订单管理列表-成功路径: 兑换品编码/名称 查询")
    def test_4_user_mgmt_order_return_queryOrder(self, exchangeNoWord, p):

        # 用例级别
        allure.dynamic.severity(p)

        data = {
            "exchangeNoWord": exchangeNoWord,
            "orderNo": "",
            "customerPhone": "",
            "customerCard": "",
            "creatorCard": "",
            "customerType": None,
            "expressType": None,
            "orderWay": None,
            "customerSource": None,
            "exchangeTimeBegin": None,
            "exchangeTimeEnd": None,
            "pageNum": 1,
            "pageSize": 10,
        }
        with _user_mgmt_order_return_queryOrder(data=data, headers=self.headers) as r:
            assert r.status_code == 200
            assert r.json()["code"] == 200
            data_list = r.json()["data"]["list"]
            assert len(data_list) > 0, "返回数据列表为空"
            if any(i.get("exchangeNoWord") is not None for i in data_list):
                assert any(i.get("exchangeNoWord") == exchangeNoWord for i in data_list)

    @pytest.mark.parametrize(
        "customerType, p", [(1, Severity.NORMAL), (2, Severity.NORMAL), (3, Severity.NORMAL), (4, Severity.NORMAL)]
    )
    @allure.title("分页查询代客售后订单管理列表-成功路径: 顾客类型 查询")
    def test_5_user_mgmt_order_return_queryOrder(self, customerType, p):

        # 用例级别
        allure.dynamic.severity(p)

        data = {
            "customerType": customerType,
            "orderNo": "",
            "customerPhone": "",
            "customerCard": "",
            "creatorCard": "",
            "exchangeNoWord": "",
            "expressType": None,
            "orderWay": None,
            "customerSource": None,
            "exchangeTimeBegin": None,
            "exchangeTimeEnd": None,
            "pageNum": 1,
            "pageSize": 10,
        }
        with _user_mgmt_order_return_queryOrder(data=data, headers=self.headers) as r:
            assert r.status_code == 200
            assert r.json()["code"] == 200
            data_list = r.json()["data"]["list"]
            assert len(data_list) > 0, "返回数据列表为空"
            if any(i.get("customerType") is not None for i in data_list):
                assert any(i.get("customerType") == customerType for i in data_list)

    @pytest.mark.parametrize("expressType, p", [(1, Severity.NORMAL), (2, Severity.NORMAL)])
    @allure.title("分页查询代客售后订单管理列表-成功路径: 配送方式 查询")
    def test_6_user_mgmt_order_return_queryOrder(self, expressType, p):

        # 用例级别
        allure.dynamic.severity(p)

        data = {
            "expressType": expressType,
            "orderNo": "",
            "customerPhone": "",
            "customerCard": "",
            "creatorCard": "",
            "exchangeNoWord": "",
            "customerType": "",
            "orderWay": None,
            "customerSource": None,
            "exchangeTimeBegin": None,
            "exchangeTimeEnd": None,
            "pageNum": 1,
            "pageSize": 10,
        }
        with _user_mgmt_order_return_queryOrder(data=data, headers=self.headers) as r:
            assert r.status_code == 200
            assert r.json()["code"] == 200
            data_list = r.json()["data"]["list"]
            assert len(data_list) > 0, "返回数据列表为空"
            if any(i.get("expressType") is not None for i in data_list):
                assert any(i.get("expressType") == expressType for i in data_list)

    @pytest.mark.parametrize("orderWay, p", [(1, Severity.NORMAL), (2, Severity.NORMAL)])
    @allure.title("分页查询代客售后订单管理列表-成功路径: 下单方式 查询")
    def test_7_user_mgmt_order_return_queryOrder(self, orderWay, p):

        # 用例级别
        allure.dynamic.severity(p)

        data = {
            "orderWay": orderWay,
            "orderNo": "",
            "customerPhone": "",
            "customerCard": "",
            "creatorCard": "",
            "exchangeNoWord": "",
            "customerType": "",
            "expressType": "",
            "customerSource": None,
            "exchangeTimeBegin": None,
            "exchangeTimeEnd": None,
            "pageNum": 1,
            "pageSize": 10,
        }
        with _user_mgmt_order_return_queryOrder(data=data, headers=self.headers) as r:
            assert r.status_code == 200
            assert r.json()["code"] == 200
            data_list = r.json()["data"]["list"]
            assert len(data_list) > 0, "返回数据列表为空"
            if any(i.get("orderWay") is not None for i in data_list):
                assert any(i.get("orderWay") == orderWay for i in data_list)

    @pytest.mark.parametrize("customerSource, p", [(0, Severity.NORMAL), (1, Severity.NORMAL), (2, Severity.NORMAL)])
    @allure.title(
        "分页查询代客售后订单管理列表-成功路径: 顾客来源平台:0->商城mall；1->健康health；2->学堂edu；4->荟友趣 查询"
    )
    def test_8_user_mgmt_order_return_queryOrder(self, customerSource, p):

        # 用例级别
        allure.dynamic.severity(p)

        data = {
            "customerSource": customerSource,
            "orderNo": "",
            "customerPhone": "",
            "customerCard": "",
            "creatorCard": "",
            "exchangeNoWord": "",
            "customerType": "",
            "expressType": "",
            "orderWay": "",
            "exchangeTimeBegin": None,
            "exchangeTimeEnd": None,
            "pageNum": 1,
            "pageSize": 10,
        }
        with _user_mgmt_order_return_queryOrder(data=data, headers=self.headers) as r:
            assert r.status_code == 200
            assert r.json()["code"] == 200
            data_list = r.json()["data"]["list"]
            assert len(data_list) > 0, "返回数据列表为空"
            if any(i.get("customerSource") is not None for i in data_list):
                assert any(i.get("customerSource") == customerSource for i in data_list)

    @pytest.mark.parametrize("exchangeTimeBegin, exchangeTimeEnd, p", [("2026-03-09", "2026-04-08", Severity.NORMAL)])
    @allure.title("分页查询代客售后订单管理列表-成功路径: 兑换时间 查询")
    def test_9_user_mgmt_order_return_queryOrder(self, exchangeTimeBegin, exchangeTimeEnd, p):

        # 用例级别
        allure.dynamic.severity(p)

        data = {
            "exchangeTimeBegin": exchangeTimeBegin,
            "exchangeTimeEnd": exchangeTimeEnd,
            "orderNo": "",
            "customerPhone": "",
            "customerCard": "",
            "creatorCard": "",
            "exchangeNoWord": "",
            "customerType": "",
            "expressType": "",
            "orderWay": "",
            "customerSource": "",
            "pageNum": 1,
            "pageSize": 10,
        }
        with _user_mgmt_order_return_queryOrder(data=data, headers=self.headers) as r:
            assert r.status_code == 200
            assert r.json()["code"] == 200
            data_list = r.json()["data"]["list"]
            assert len(data_list) > 0, "返回数据列表为空"

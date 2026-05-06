import os

import allure
import pytest
from allure_commons.types import Severity

from apis.mall_center_user import _user_mgmt_order_page


@pytest.mark.test_4295
@allure.epic("mall_center_user")
@allure.feature("建议输入被测业务功能模块，如订单管理")
@allure.story("/user/mgmt/order/page")
@allure.description("""接口说明：
- 接口名称：分页查询兑换订单列表
- 接口地址：/user/mgmt/order/page

主要参数说明：
- customerType：顾客类型 1->普通顾客 2->优惠顾客 3->云商 4->微店 5->云+子账号
- commitTimeEnd：提交时间-结束
- creatorCard：开单人卡号
- pageNum：# TODO 请填写参数备注
- commitTimeBegin：提交时间-开始
- pageSize：# TODO 请填写参数备注
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

    @pytest.mark.parametrize(
        "customerType, p", [(1, Severity.NORMAL), (2, Severity.NORMAL), (3, Severity.NORMAL), (4, Severity.NORMAL)]
    )
    @allure.title("分页查询兑换订单列表-成功路径: 顾客类型 查询")
    def test_0_user_mgmt_order_page(self, customerType, p):

        # 用例级别
        allure.dynamic.severity(p)

        data = {
            "customerType": customerType,
            "orderNo": None,
            "companyWord": None,
            "orderStatusList": [],
            "customerPhone": None,
            "customerCard": None,
            "customerName": None,
            "exchangeNoWord": None,
            "customerSourceList": [],
            "creatorCard": None,
            "expressType": None,
            "orderWay": None,
            "exchangeTimeBegin": None,
            "exchangeTimeEnd": None,
            "commitTimeBegin": None,
            "commitTimeEnd": None,
            "payTimeBegin": None,
            "payTimeEnd": None,
            "cancelTimeBegin": None,
            "cancelTimeEnd": None,
            "hxTimeBegin": None,
            "hxTimeEnd": None,
            "pageNum": 1,
            "pageSize": 10,
        }
        with _user_mgmt_order_page(data=data, headers=self.headers) as r:
            assert r.status_code == 200
            assert r.json()["code"] == 200
            data_list = r.json()["data"]["list"]
            assert len(data_list) > 0, "返回数据列表为空"
            if any(i.get("customerType") is not None for i in data_list):
                assert any(i.get("customerType") == customerType for i in data_list)

    @pytest.mark.parametrize("creatorCard, p", [("3000470099", Severity.NORMAL)])
    @allure.title("分页查询兑换订单列表-成功路径: 开单人卡号 查询")
    def test_1_user_mgmt_order_page(self, creatorCard, p):

        # 用例级别
        allure.dynamic.severity(p)

        data = {
            "creatorCard": creatorCard,
            "orderNo": None,
            "companyWord": None,
            "orderStatusList": [],
            "customerPhone": None,
            "customerCard": None,
            "customerName": None,
            "exchangeNoWord": None,
            "customerType": "",
            "customerSourceList": [],
            "expressType": None,
            "orderWay": None,
            "exchangeTimeBegin": None,
            "exchangeTimeEnd": None,
            "commitTimeBegin": None,
            "commitTimeEnd": None,
            "payTimeBegin": None,
            "payTimeEnd": None,
            "cancelTimeBegin": None,
            "cancelTimeEnd": None,
            "hxTimeBegin": None,
            "hxTimeEnd": None,
            "pageNum": 1,
            "pageSize": 10,
        }
        with _user_mgmt_order_page(data=data, headers=self.headers) as r:
            assert r.status_code == 200
            assert r.json()["code"] == 200
            data_list = r.json()["data"]["list"]
            assert len(data_list) > 0, "返回数据列表为空"
            if any(i.get("creatorCard") is not None for i in data_list):
                assert any(i.get("creatorCard") == creatorCard for i in data_list)

    @pytest.mark.parametrize("commitTimeBegin, commitTimeEnd, p", [("2026-04-01", "2026-04-29", Severity.NORMAL)])
    @allure.title("分页查询兑换订单列表-成功路径: 提交时间 查询")
    def test_2_user_mgmt_order_page(self, commitTimeBegin, commitTimeEnd, p):

        # 用例级别
        allure.dynamic.severity(p)

        data = {
            "commitTimeBegin": commitTimeBegin,
            "commitTimeEnd": commitTimeEnd,
            "orderNo": None,
            "companyWord": None,
            "orderStatusList": [],
            "customerPhone": None,
            "customerCard": None,
            "customerName": None,
            "exchangeNoWord": None,
            "customerType": "",
            "customerSourceList": [],
            "creatorCard": "",
            "expressType": None,
            "orderWay": None,
            "exchangeTimeBegin": None,
            "exchangeTimeEnd": None,
            "payTimeBegin": None,
            "payTimeEnd": None,
            "cancelTimeBegin": None,
            "cancelTimeEnd": None,
            "hxTimeBegin": None,
            "hxTimeEnd": None,
            "pageNum": 1,
            "pageSize": 10,
        }
        with _user_mgmt_order_page(data=data, headers=self.headers) as r:
            assert r.status_code == 200
            assert r.json()["code"] == 200
            data_list = r.json()["data"]["list"]
            assert len(data_list) > 0, "返回数据列表为空"

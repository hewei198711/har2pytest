# 自动生成的pytest用例文件
# 基于HAR文件: 兑换订单管理.har
# 生成时间: 2026-04-29 11:09:56.201141

import os

import allure
import pytest
from setting import P2

from apis.mall_center_user._user_mgmt_order_page import _user_mgmt_order_page


@allure.feature("mall_center_user")
@allure.story("/user/mgmt/order/page")
@allure.description("""接口说明：
- 接口名称：分页查询兑换订单列表
- 接口地址：/user/mgmt/order/page

主要参数说明：
- exchangeTimeEnd：兑换时间-结束
- cancelTimeEnd：取消时间-结束
- expressType：配送方式 1->服务中心自提 2->公司配送
- hxTimeBegin：核销时间-开始
- creatorCard：开单人卡号
- customerName：顾客姓名
- customerCard：顾客卡号
- customerPhone：顾客手机号
- customerType：顾客类型 1->普通顾客 2->优惠顾客 3->云商 4->微店 5->云+子账号
- hxTimeEnd：核销时间-结束
- pageSize：# TODO 请填写参数备注
- commitTimeEnd：提交时间-结束
- commitTimeBegin：提交时间-开始
- exchangeNoWord：兑换品编码/名称
- exchangeTimeBegin：兑换时间-开始
- payTimeBegin：付款时间-开始
- customerSourceList：顾客来源平台:0->商城mall；1->健康health；2->学堂edu；4->荟友趣
- payTimeEnd：付款时间-结束
- orderNo：兑换流水号
- companyWord：业务分公司编码/名称
- cancelTimeBegin：取消时间-开始
- pageNum：# TODO 请填写参数备注
- orderWay：下单方式 1->自购订单 2->代购订单
- orderStatusList：订单状态 1->待支付 2->待发货 3->待收货(已发货) 4->已取消 5->已退货 6->待核销 99->已完成

业务场景：
1. 成功路径：使用各种条件查询订单列表
2. 验证逻辑：返回列表数据，验证code=200
3. 测试数据清理：无副作用，仅查询数据
""")
class TestClass:
    """
    基于HAR文件 兑换订单管理.har 的API流程测试
    每个API请求作为一个测试步骤
    """

    # 初始化测试数据字典，用于在步骤间传递数据
    def setup_class(self):
        self.access_token = os.environ["access_token"]

    @pytest.mark.test_4291
    @pytest.mark.parametrize("customerType, p", [(1, P2), (2, P2), (3, P2), (4, P2)])
    @allure.title("分页查询兑换订单列表-成功路径: 顾客来源平台:0-订单状态 1-顾客类型 1 查询")
    def test_0_user_mgmt_order_page(self, customerType, p):

        # 用例级别
        allure.dynamic.severity(p)

        data = {
            "customerSourceList": [],
            "customerType": customerType,
            "orderStatusList": [],
            "orderNo": None,
            "companyWord": None,
            "customerPhone": None,
            "customerCard": None,
            "customerName": None,
            "exchangeNoWord": None,
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
        with _user_mgmt_order_page(access_token=self.access_token, data=data) as r:
            assert r.status_code == 200
            assert r.json()["code"] == 200
            data_list = r.json()["data"]["list"]
            assert len(data_list) > 0, "返回数据列表为空"
            if any(i.get("customerType") is not None for i in data_list):
                assert any(i.get("customerType") == customerType for i in data_list)

    @pytest.mark.test_4291
    @pytest.mark.parametrize("creatorCard, p", [("3000470099", P2)])
    @allure.title("分页查询兑换订单列表-成功路径: 开单人卡号 查询")
    def test_1_user_mgmt_order_page(self, creatorCard, p):

        # 用例级别
        allure.dynamic.severity(p)

        data = {
            "customerSourceList": [],
            "customerType": None,
            "orderStatusList": [],
            "orderNo": None,
            "companyWord": None,
            "customerPhone": None,
            "customerCard": None,
            "customerName": None,
            "exchangeNoWord": None,
            "creatorCard": creatorCard,
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
        with _user_mgmt_order_page(access_token=self.access_token, data=data) as r:
            assert r.status_code == 200
            assert r.json()["code"] == 200
            data_list = r.json()["data"]["list"]
            assert len(data_list) > 0, "返回数据列表为空"
            if any(i.get("creatorCard") is not None for i in data_list):
                assert any(i.get("creatorCard") == creatorCard for i in data_list)

    @pytest.mark.test_4291
    @pytest.mark.parametrize("commitTimeBegin, commitTimeEnd, p", [("2026-04-01", "2026-04-29", P2)])
    @allure.title("分页查询兑换订单列表-成功路径: 提交时间  {commitTimeBegin}-{commitTimeEnd} 查询")
    def test_2_user_mgmt_order_page(self, commitTimeBegin, commitTimeEnd, p):

        # 用例级别
        allure.dynamic.severity(p)

        data = {
            "customerSourceList": [],
            "customerType": None,
            "orderStatusList": [],
            "orderNo": None,
            "companyWord": None,
            "customerPhone": None,
            "customerCard": None,
            "customerName": None,
            "exchangeNoWord": None,
            "creatorCard": None,
            "expressType": None,
            "orderWay": None,
            "exchangeTimeBegin": None,
            "exchangeTimeEnd": None,
            "commitTimeBegin": commitTimeBegin,
            "commitTimeEnd": commitTimeEnd,
            "payTimeBegin": None,
            "payTimeEnd": None,
            "cancelTimeBegin": None,
            "cancelTimeEnd": None,
            "hxTimeBegin": None,
            "hxTimeEnd": None,
            "pageNum": 1,
            "pageSize": 10,
        }
        with _user_mgmt_order_page(access_token=self.access_token, data=data) as r:
            assert r.status_code == 200
            assert r.json()["code"] == 200
            data_list = r.json()["data"]["list"]
            assert len(data_list) > 0, "返回数据列表为空"




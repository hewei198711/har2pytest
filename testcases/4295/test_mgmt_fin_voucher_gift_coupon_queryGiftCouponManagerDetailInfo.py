import os

import allure
import pytest
from allure_commons.types import Severity

from apis.mall_mgmt_application import _mgmt_fin_voucher_gift_coupon_queryGiftCouponManagerDetailInfo


@pytest.mark.test_4295
@allure.epic("mall_mgmt_application")
@allure.feature("建议输入被测业务功能模块，如订单管理")
@allure.story("/mgmt/fin/voucher/gift/coupon/queryGiftCouponManagerDetailInfo")
@allure.description("""接口说明：
- 接口名称：电子礼券管理界面查询详情接口（商城后台）
- 接口地址：/mgmt/fin/voucher/gift/coupon/queryGiftCouponManagerDetailInfo

主要参数说明：
- grantdtlId：电子礼券发放id号
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

    @pytest.mark.parametrize("grantdtlId, p", [("2043868590615973888", Severity.NORMAL)])
    @allure.title("电子礼券管理界面查询详情接口（商城后台）-成功路径: 电子礼券发放id号 查询")
    def test_0_mgmt_fin_voucher_gift_coupon_queryGiftCouponManagerDetailInfo(self, grantdtlId, p):

        # 用例级别
        allure.dynamic.severity(p)

        data = {
            "grantdtlId": grantdtlId,
        }
        with _mgmt_fin_voucher_gift_coupon_queryGiftCouponManagerDetailInfo(data=data, headers=self.headers) as r:
            assert r.status_code == 200
            assert r.json()["code"] == 200
            data_list = r.json()["data"]["list"]
            assert len(data_list) > 0, "返回数据列表为空"
            if any(i.get("grantdtlId") is not None for i in data_list):
                assert any(i.get("grantdtlId") == grantdtlId for i in data_list)

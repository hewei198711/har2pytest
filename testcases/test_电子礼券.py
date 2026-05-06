import os

import allure
from allure_commons.types import Severity

from apis.mall_mgmt_application import _mgmt_fin_voucher_gift_coupon_queryGiftCouponManagerDetailInfo


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

    @allure.step("电子礼券管理界面查询详情接口（商城后台）")
    def step_mgmt_fin_voucher_gift_coupon_queryGiftCouponManagerDetailInfo():

        data = {"grantdtlId": "2043868590615973888"}
        with _mgmt_fin_voucher_gift_coupon_queryGiftCouponManagerDetailInfo(
            data=data, headers=test_data["headers"]
        ) as r:
            assert r.status_code == 200
            assert r.json()["code"] == 200
            test_data["coupon_queryGiftCouponManagerDetailInfo"] = r.json()

    # 执行所有测试步骤
    step_mgmt_fin_voucher_gift_coupon_queryGiftCouponManagerDetailInfo()

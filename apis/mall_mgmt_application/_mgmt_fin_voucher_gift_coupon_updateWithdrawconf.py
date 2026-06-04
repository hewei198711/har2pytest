import os

from util.client import client

data = {
    "id": 0,  # 主键id
    "minAmount": 0.0,  # 单次提现合计金额下限
    "remark": "",  # 提现说明
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_fin_voucher_gift_coupon_updateWithdrawconf(data=data, headers=headers):
    """
    电子礼券提现配置修改
    /mgmt/fin/voucher/gift/coupon/updateWithdrawconf

    参数说明:
    - id: 主键id
    - minAmount: 单次提现合计金额下限
    - remark: 提现说明
    """

    url = "/mgmt/fin/voucher/gift/coupon/updateWithdrawconf"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

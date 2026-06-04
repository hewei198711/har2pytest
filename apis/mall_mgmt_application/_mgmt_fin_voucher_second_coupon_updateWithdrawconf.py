import os

from util.client import client

data = {
    "id": 0,  # 主键id
    "maxNum": 0,  # 每月提现次数上限
    "minAmount": 0.0,  # 单次提现合计金额下限
    "remark": "",  # 提现说明
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_fin_voucher_second_coupon_updateWithdrawconf(data=data, headers=headers):
    """
    秒返券提现配置修改
    /mgmt/fin/voucher/second/coupon/updateWithdrawconf

    参数说明:
    - id: 主键id
    - maxNum: 每月提现次数上限
    - minAmount: 单次提现合计金额下限
    - remark: 提现说明
    """

    url = "/mgmt/fin/voucher/second/coupon/updateWithdrawconf"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

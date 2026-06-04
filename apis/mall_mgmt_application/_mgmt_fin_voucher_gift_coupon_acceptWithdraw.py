import os

from util.client import client

data = {
    "idList": [],  # 主键id集合
    "remark": "",  # 备注
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_fin_voucher_gift_coupon_acceptWithdraw(data=data, headers=headers):
    """
    电子礼券提现受理接口
    /mgmt/fin/voucher/gift/coupon/acceptWithdraw

    参数说明:
    - idList: 主键id集合
    - remark: 备注
    """

    url = "/mgmt/fin/voucher/gift/coupon/acceptWithdraw"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

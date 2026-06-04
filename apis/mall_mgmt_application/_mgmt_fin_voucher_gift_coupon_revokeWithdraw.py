import os

from util.client import client

data = {
    "id": 0,  # 主键id
    "platformType": 0,  # 平台类型，前端无需传递此参数
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_fin_voucher_gift_coupon_revokeWithdraw(data=data, headers=headers):
    """
    电子礼券提现撤销接口
    /mgmt/fin/voucher/gift/coupon/revokeWithdraw

    参数说明:
    - id: 主键id
    - platformType: 平台类型，前端无需传递此参数
    """

    url = "/mgmt/fin/voucher/gift/coupon/revokeWithdraw"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

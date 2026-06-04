import os

from util.client import client

data = {
    "grantTimeStr": "",  # 派发时间，格式：yyyy-MM-dd HH:mm
    "grantWay": 0,  # 派发方式，1：即时派发；2：定时派发
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_fin_voucher_mgmtGrantSecondCoupon(data=data, headers=headers):
    """
    购物礼券派发管理派发
    /mgmt/fin/voucher/mgmtGrantSecondCoupon

    参数说明:
    - grantTimeStr: 派发时间，格式：yyyy-MM-dd HH:mm
    - grantWay: 派发方式，1：即时派发；2：定时派发
    """

    url = "/mgmt/fin/voucher/mgmtGrantSecondCoupon"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

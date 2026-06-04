import os

from util.client import client

data = {
    "from": 0,  # TODO: 添加参数说明
    "granterName": "",  # 操作人
    "orderMonthEnd": "",  # 业绩月份结束
    "orderMonthStart": "",  # 业绩月份开始
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 每页显示数
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_fin_voucher_getSecondCouponGrant(data=data, headers=headers):
    """
    购物礼券派发管理
    /mgmt/fin/voucher/getSecondCouponGrant

    参数说明:
    - granterName: 操作人
    - orderMonthEnd: 业绩月份结束
    - orderMonthStart: 业绩月份开始
    - pageNum: 页数
    - pageSize: 每页显示数
    """

    url = "/mgmt/fin/voucher/getSecondCouponGrant"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

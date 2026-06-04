import os

from util.client import client

params = {
    "cardNo": "",  # cardNo
    "pageNum": 0,  # pageNum
    "pageSize": 0,  # pageSize
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_fin_voucher_getGiftCouponByCardNo(params=params, headers=headers):
    """
    顾客查询-查询电子礼券发放信息
    /mgmt/fin/voucher/getGiftCouponByCardNo

    参数说明:
    - cardNo: cardNo
    - pageNum: pageNum
    - pageSize: pageSize
    """

    url = "/mgmt/fin/voucher/getGiftCouponByCardNo"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

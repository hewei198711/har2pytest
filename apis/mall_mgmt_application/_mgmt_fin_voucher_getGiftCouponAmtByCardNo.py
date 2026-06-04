import os

from util.client import client

params = {
    "cardNo": "",  # cardNo
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_fin_voucher_getGiftCouponAmtByCardNo(params=params, headers=headers):
    """
    顾客查询-查询电子礼券总金额信息
    /mgmt/fin/voucher/getGiftCouponAmtByCardNo

    参数说明:
    - cardNo: cardNo
    """

    url = "/mgmt/fin/voucher/getGiftCouponAmtByCardNo"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

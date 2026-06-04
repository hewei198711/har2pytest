import os

from util.client import client

params = {
    "couponNameOrNumber": "",  # couponNameOrNumber
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_signSalePlus_selectSignSaleGrantCoupon(params=params, headers=headers):
    """
    搜索签约购活动派发的优惠券
    /mgmt/prmt/signSalePlus/selectSignSaleGrantCoupon

    参数说明:
    - couponNameOrNumber: couponNameOrNumber
    """

    url = "/mgmt/prmt/signSalePlus/selectSignSaleGrantCoupon"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_prmt_coupon_importPromotion(headers=headers):
    """
    导入活动
    /mgmt/prmt/coupon/importPromotion
    """

    url = "/mgmt/prmt/coupon/importPromotion"
    with client.post(url=url, headers=headers) as r:
        return r

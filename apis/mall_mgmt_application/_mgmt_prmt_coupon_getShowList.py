import os

from util.client import client

headers = {
    "channel": "pc",
    "client": "op",
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_prmt_coupon_getShowList(headers=headers):
    """
    商品分类列表
    /mgmt/prmt/coupon/getShowList
    """

    url = "/mgmt/prmt/coupon/getShowList"
    with client.get(url=url, headers=headers) as r:
        return r

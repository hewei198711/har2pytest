import os

from util.client import client

params = {
    "serialNo": "",  # 商品编码
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_sendGift_selectProduct(params=params, headers=headers):
    """
    搜索送礼活动商品
    /mgmt/prmt/sendGift/selectProduct

    参数说明:
    - serialNo: 商品编码
    """

    url = "/mgmt/prmt/sendGift/selectProduct"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

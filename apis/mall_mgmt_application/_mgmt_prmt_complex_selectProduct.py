import os

from util.client import client

params = {
    "isGift": False,  # 是否查询赠品
    "serialNo": "",  # 商品编码
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_complex_selectProduct(params=params, headers=headers):
    """
    查询签约购活动商品或者赠品
    /mgmt/prmt/complex/selectProduct

    参数说明:
    - isGift: 是否查询赠品
    - serialNo: 商品编码
    """

    url = "/mgmt/prmt/complex/selectProduct"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

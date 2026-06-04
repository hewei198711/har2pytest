import os

from util.client import client

params = {
    "serialNo": "",  # serialNo
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_signSalePlus_selectSignSaleProduct(params=params, headers=headers):
    """
    查询签约购活动商品
    /mgmt/prmt/signSalePlus/selectSignSaleProduct

    参数说明:
    - serialNo: serialNo
    """

    url = "/mgmt/prmt/signSalePlus/selectSignSaleProduct"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

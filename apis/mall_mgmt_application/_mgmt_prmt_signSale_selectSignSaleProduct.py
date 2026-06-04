import os

from util.client import client

params = {
    "serialNo": "",  # serialNo
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_signSale_selectSignSaleProduct(params=params, headers=headers):
    """
    查询签约购商品
    /mgmt/prmt/signSale/selectSignSaleProduct

    参数说明:
    - serialNo: serialNo
    """

    url = "/mgmt/prmt/signSale/selectSignSaleProduct"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

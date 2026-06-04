import os

from util.client import client

params = {
    "serialNo": "",  # serialNo
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_signSale_selectSignSaleGift(params=params, headers=headers):
    """
    搜索签约购活动赠品：签约赠品/续约福利
    /mgmt/prmt/signSale/selectSignSaleGift

    参数说明:
    - serialNo: serialNo
    """

    url = "/mgmt/prmt/signSale/selectSignSaleGift"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

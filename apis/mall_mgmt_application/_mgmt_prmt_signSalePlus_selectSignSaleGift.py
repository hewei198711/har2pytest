import os

from util.client import client

params = {
    "serialNo": "",  # serialNo
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_signSalePlus_selectSignSaleGift(params=params, headers=headers):
    """
    搜索签约购活动赠品
    /mgmt/prmt/signSalePlus/selectSignSaleGift

    参数说明:
    - serialNo: serialNo
    """

    url = "/mgmt/prmt/signSalePlus/selectSignSaleGift"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

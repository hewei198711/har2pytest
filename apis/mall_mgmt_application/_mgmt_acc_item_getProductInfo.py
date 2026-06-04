import os

from util.client import client

params = {
    "serialNo": "",  # serialNo
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_acc_item_getProductInfo(params=params, headers=headers):
    """
    根据商品编码查询产品
    /mgmt/acc/item/getProductInfo

    参数说明:
    - serialNo: serialNo
    """

    url = "/mgmt/acc/item/getProductInfo"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

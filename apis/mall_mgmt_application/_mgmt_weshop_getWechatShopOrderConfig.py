import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_weshop_getWechatShopOrderConfig(headers=headers):
    """
    订单超时设置-微信小店
    /mgmt/weshop/getWechatShopOrderConfig
    """

    url = "/mgmt/weshop/getWechatShopOrderConfig"
    with client.get(url=url, headers=headers) as r:
        return r

import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_weshop_getWechatShopShowConfig(headers=headers):
    """
    微信小店转分控制（显示标识，1：显示；2：隐藏）
    /mgmt/weshop/getWechatShopShowConfig
    """

    url = "/mgmt/weshop/getWechatShopShowConfig"
    with client.get(url=url, headers=headers) as r:
        return r

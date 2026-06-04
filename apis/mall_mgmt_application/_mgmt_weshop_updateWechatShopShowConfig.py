import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_weshop_updateWechatShopShowConfig(headers=headers):
    """
    修改微信小店转分控制
    /mgmt/weshop/updateWechatShopShowConfig
    """

    url = "/mgmt/weshop/updateWechatShopShowConfig"
    with client.post(url=url, headers=headers) as r:
        return r

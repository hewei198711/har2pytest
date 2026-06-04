import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_weshop_getWechatShopShowConfigLog(headers=headers):
    """
    微信小店转分控制修改记录
    /mgmt/weshop/getWechatShopShowConfigLog
    """

    url = "/mgmt/weshop/getWechatShopShowConfigLog"
    with client.post(url=url, headers=headers) as r:
        return r

import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_order_getGygPromMedalOption(headers=headers):
    """
    公益购活动详情-勋章等级筛选条件
    /mgmt/order/getGygPromMedalOption
    """

    url = "/mgmt/order/getGygPromMedalOption"
    with client.get(url=url, headers=headers) as r:
        return r

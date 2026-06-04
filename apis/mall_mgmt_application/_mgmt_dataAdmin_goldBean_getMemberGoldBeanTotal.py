import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_dataAdmin_goldBean_getMemberGoldBeanTotal(headers=headers):
    """
    用户持有金豆总数
    /mgmt/dataAdmin/goldBean/getMemberGoldBeanTotal
    """

    url = "/mgmt/dataAdmin/goldBean/getMemberGoldBeanTotal"
    with client.get(url=url, headers=headers) as r:
        return r

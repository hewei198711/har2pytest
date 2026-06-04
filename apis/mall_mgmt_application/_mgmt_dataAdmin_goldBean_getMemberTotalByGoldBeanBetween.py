import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_dataAdmin_goldBean_getMemberTotalByGoldBeanBetween(headers=headers):
    """
    金豆持有区间
    /mgmt/dataAdmin/goldBean/getMemberTotalByGoldBeanBetween
    """

    url = "/mgmt/dataAdmin/goldBean/getMemberTotalByGoldBeanBetween"
    with client.get(url=url, headers=headers) as r:
        return r

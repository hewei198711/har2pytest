import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_dataAdmin_goldBean_getDistributeChannelList(headers=headers):
    """
    金豆发放统计-发放渠道列表
    /mgmt/dataAdmin/goldBean/getDistributeChannelList
    """

    url = "/mgmt/dataAdmin/goldBean/getDistributeChannelList"
    with client.get(url=url, headers=headers) as r:
        return r

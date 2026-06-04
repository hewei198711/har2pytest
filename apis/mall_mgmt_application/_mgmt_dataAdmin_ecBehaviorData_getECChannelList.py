import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_dataAdmin_ecBehaviorData_getECChannelList(headers=headers):
    """
    获取兑换中心渠道列表
    /mgmt/dataAdmin/ecBehaviorData/getECChannelList
    """

    url = "/mgmt/dataAdmin/ecBehaviorData/getECChannelList"
    with client.get(url=url, headers=headers) as r:
        return r

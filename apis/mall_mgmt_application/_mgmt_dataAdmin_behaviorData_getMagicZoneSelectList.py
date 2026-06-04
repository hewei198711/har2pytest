import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_dataAdmin_behaviorData_getMagicZoneSelectList(headers=headers):
    """
    查询专区下拉框列表
    /mgmt/dataAdmin/behaviorData/getMagicZoneSelectList
    """

    url = "/mgmt/dataAdmin/behaviorData/getMagicZoneSelectList"
    with client.get(url=url, headers=headers) as r:
        return r

import os

from util.client import client

params = {
    "includeAll": "",  # 是否包含全部 0/null 否 1.是
    "zoneId": "",  # 分区id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_dataAdmin_behaviorData_getZonePictAdSelectList(params=params, headers=headers):
    """
    查询专区图片广告下拉框列表
    /mgmt/dataAdmin/behaviorData/getZonePictAdSelectList

    参数说明:
    - includeAll: 是否包含全部 0/null 否 1.是
    - zoneId: 分区id
    """

    url = "/mgmt/dataAdmin/behaviorData/getZonePictAdSelectList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

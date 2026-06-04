import os

from util.client import client

params = {
    "day": 0,  # day
    "type": 0,  # type
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_dataAdmin_userData_platform_list(params=params, headers=headers):
    """
    查询用户平台百分比
    /mgmt/dataAdmin/userData/platform/list

    参数说明:
    - day: day
    - type: type
    """

    url = "/mgmt/dataAdmin/userData/platform/list"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

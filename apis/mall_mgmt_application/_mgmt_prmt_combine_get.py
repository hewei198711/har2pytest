import os

from util.client import client

params = {
    "getLogs": False,  # 是否获取操作记录
    "id": "",  # 活动id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_combine_get(params=params, headers=headers):
    """
    获取活动详情(详情或编辑回显)
    /mgmt/prmt/combine/get

    参数说明:
    - getLogs: 是否获取操作记录
    - id: 活动id
    """

    url = "/mgmt/prmt/combine/get"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

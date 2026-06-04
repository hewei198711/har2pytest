import os

from util.client import client

params = {
    "getLogs": False,  # 是否获取操作记录
    "id": "",  # 派发任务id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_couponPackage_get(params=params, headers=headers):
    """
    获取派发任务(详情或编辑回显)
    /mgmt/prmt/couponPackage/get

    参数说明:
    - getLogs: 是否获取操作记录
    - id: 派发任务id
    """

    url = "/mgmt/prmt/couponPackage/get"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

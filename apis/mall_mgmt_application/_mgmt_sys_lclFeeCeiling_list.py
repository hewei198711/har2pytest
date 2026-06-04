import os

from util.client import client

params = {
    "status": 0,  # 启用状态(0:禁用；1：启用)
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_lclFeeCeiling_list(params=params, headers=headers):
    """
    获取拼箱费模板上限列表
    /mgmt/sys/lclFeeCeiling/list

    参数说明:
    - status: 启用状态(0:禁用；1：启用)
    """

    url = "/mgmt/sys/lclFeeCeiling/list"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

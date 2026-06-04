import os

from util.client import client

params = {
    "type": "",  # 1、形象手册管理 2、油葱微店运营与管理手册 3、服务中心运营与管理手册 4、优秀案例库
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_manual_detail(params=params, headers=headers):
    """
    获取形象手册详情
    /mgmt/sys/manual/detail

    参数说明:
    - type: 1、形象手册管理 2、油葱微店运营与管理手册 3、服务中心运营与管理手册 4、优秀案例库
    """

    url = "/mgmt/sys/manual/detail"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

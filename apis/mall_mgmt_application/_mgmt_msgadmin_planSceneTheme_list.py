import os

from util.client import client

params = {
    "status": 0,  # status
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_msgadmin_planSceneTheme_list(params=params, headers=headers):
    """
    业务主题列表
    /mgmt/msgadmin/planSceneTheme/list

    参数说明:
    - status: status
    """

    url = "/mgmt/msgadmin/planSceneTheme/list"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

import os

from util.client import client

params = {
    "planSceneId": 0,  # planSceneId
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_msgadmin_planSceneTheme_get(params=params, headers=headers):
    """
    get
    /mgmt/msgadmin/planSceneTheme/get

    参数说明:
    - planSceneId: planSceneId
    """

    url = "/mgmt/msgadmin/planSceneTheme/get"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_role_authModules(headers=headers):
    """
    权限明细
    /appStore/role/authModules
    """

    url = "/appStore/role/authModules"
    with client.get(url=url, headers=headers) as r:
        return r

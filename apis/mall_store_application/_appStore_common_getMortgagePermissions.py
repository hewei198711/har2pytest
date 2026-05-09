import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _appStore_common_getMortgagePermissions(headers=headers):
    """
    查询服务中心的押货&售后相关权限
    /appStore/common/getMortgagePermissions
    """

    url = "/appStore/common/getMortgagePermissions"
    with client.get(url=url, headers=headers) as r:
        return r

import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _appStore_common_getCompanyList(headers=headers):
    """
    获取分公司列表
    /appStore/common/getCompanyList
    """

    url = "/appStore/common/getCompanyList"
    with client.get(url=url, headers=headers) as r:
        return r

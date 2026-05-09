import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _appStore_common_fetchStoreAndCompanyInfo(headers=headers):
    """
    获取上门取件相关默认参数
    /appStore/common/fetchStoreAndCompanyInfo
    """

    url = "/appStore/common/fetchStoreAndCompanyInfo"
    with client.get(url=url, headers=headers) as r:
        return r

import os

from util.client import client

params = {
    "storeCode": "",  # storeCode
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_web_contract_getStoreAuthStatus(params=params, headers=headers):
    """
    查询服务中心企业认证状态
    /appStore/web/contract/getStoreAuthStatus

    参数说明:
    - storeCode: storeCode
    """

    url = "/appStore/web/contract/getStoreAuthStatus"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

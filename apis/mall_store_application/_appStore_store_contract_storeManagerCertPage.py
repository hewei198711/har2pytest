import os

from util.client import client

params = {
    "storeCode": "",  # 服务中心编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_contract_storeManagerCertPage(params=params, headers=headers):
    """
    服务中心管理员实名认证页面
    /appStore/store/contract/storeManagerCertPage

    参数说明:
    - storeCode: 服务中心编号
    """

    url = "/appStore/store/contract/storeManagerCertPage"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

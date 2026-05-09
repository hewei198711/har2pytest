import os

from util.client import client

params = {
    "reCert": "",  # 是否重新认证，1、首次认证（默认），2、重新认证
    "storeCode": "",  # 服务中心编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_web_contract_storeCertificationPage(params=params, headers=headers):
    """
    服务中心实名认证页面
    /appStore/web/contract/storeCertificationPage

    参数说明:
    - reCert: 是否重新认证，1、首次认证（默认），2、重新认证
    - storeCode: 服务中心编号
    """

    url = "/appStore/web/contract/storeCertificationPage"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

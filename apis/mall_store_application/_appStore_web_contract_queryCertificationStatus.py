import os

from util.client import client

params = {
    "storeCode": "",  # 服务中心编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_web_contract_queryCertificationStatus(params=params, headers=headers):
    """
    查询服务中心实名认证状态
    /appStore/web/contract/queryCertificationStatus

    参数说明:
    - storeCode: 服务中心编号
    """

    url = "/appStore/web/contract/queryCertificationStatus"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

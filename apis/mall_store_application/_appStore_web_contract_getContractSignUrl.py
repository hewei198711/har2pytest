import os

from util.client import client

params = {
    "docNo": "",  # docNo
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_web_contract_getContractSignUrl(params=params, headers=headers):
    """
    获取已生成合同的合同签署链接
    /appStore/web/contract/getContractSignUrl

    参数说明:
    - docNo: docNo
    """

    url = "/appStore/web/contract/getContractSignUrl"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

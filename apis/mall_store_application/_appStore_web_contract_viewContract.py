import os

from util.client import client

params = {
    "docNo": "",  # 合同编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_web_contract_viewContract(params=params, headers=headers):
    """
    合同查看
    /appStore/web/contract/viewContract

    参数说明:
    - docNo: 合同编号
    """

    url = "/appStore/web/contract/viewContract"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

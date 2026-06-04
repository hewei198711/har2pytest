import os

from util.client import client

params = {
    "docNo": "",  # 合同编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_viewContract(params=params, headers=headers):
    """
    查看合同
    /mgmt/store/viewContract

    参数说明:
    - docNo: 合同编号
    """

    url = "/mgmt/store/viewContract"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

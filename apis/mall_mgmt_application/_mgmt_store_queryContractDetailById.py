import os

from util.client import client

params = {
    "id": "",  # 主键id(必填)
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_queryContractDetailById(params=params, headers=headers):
    """
    查看合同详情
    /mgmt/store/queryContractDetailById

    参数说明:
    - id: 主键id(必填)
    """

    url = "/mgmt/store/queryContractDetailById"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

import os

from util.client import client

data = {
    "id": 0,  # id
    "identifyStatus": 0,  # 识别状态 1识别通过 2拒绝通过
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_storeContractBankCard_identify(data=data, headers=headers):
    """
    识别/重新识别
    /mgmt/store/storeContractBankCard/identify

    参数说明:
    - id: id
    - identifyStatus: 识别状态 1识别通过 2拒绝通过
    """

    url = "/mgmt/store/storeContractBankCard/identify"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

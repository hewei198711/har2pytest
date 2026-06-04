import os

from util.client import client

data = {
    "docNos": [],  # 合同编号集合
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_contract_batchRetryStoreContractInvtBill(data=data, headers=headers):
    """
    批量重试对账单电子合同
    /mgmt/store/contract/batchRetryStoreContractInvtBill

    参数说明:
    - docNos: 合同编号集合
    """

    url = "/mgmt/store/contract/batchRetryStoreContractInvtBill"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

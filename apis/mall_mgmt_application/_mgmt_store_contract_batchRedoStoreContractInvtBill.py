import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_store_contract_batchRedoStoreContractInvtBill(headers=headers):
    """
    批量撤回对账单电子合同
    /mgmt/store/contract/batchRedoStoreContractInvtBill
    """

    url = "/mgmt/store/contract/batchRedoStoreContractInvtBill"
    with client.post(url=url, headers=headers) as r:
        return r

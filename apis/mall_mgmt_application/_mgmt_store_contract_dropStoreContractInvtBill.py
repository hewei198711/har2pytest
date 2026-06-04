import os
from urllib.parse import urlencode

from util.client import client

data = {
    "docNo": "",  # docNo
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_store_contract_dropStoreContractInvtBill(data=data, headers=headers):
    """
    作废对账单电子合同
    /mgmt/store/contract/dropStoreContractInvtBill

    参数说明:
    - docNo: docNo
    """

    url = "/mgmt/store/contract/dropStoreContractInvtBill"
    data = urlencode(data)  # application/x-www-form-urlencoded传参需要特殊处理

    with client.post(url=url, data=data, headers=headers) as r:
        return r

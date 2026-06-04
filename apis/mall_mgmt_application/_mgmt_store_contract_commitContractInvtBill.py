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


def _mgmt_store_contract_commitContractInvtBill(data=data, headers=headers):
    """
    提交库存对账单合同
    /mgmt/store/contract/commitContractInvtBill

    参数说明:
    - docNo: docNo
    """

    url = "/mgmt/store/contract/commitContractInvtBill"
    data = urlencode(data)  # application/x-www-form-urlencoded传参需要特殊处理

    with client.post(url=url, data=data, headers=headers) as r:
        return r

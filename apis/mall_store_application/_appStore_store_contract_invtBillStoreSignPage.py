import os

from util.client import client

params = {
    "docNo": "",  # docNo
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_contract_invtBillStoreSignPage(params=params, headers=headers):
    """
    库存对账单电子合同店铺签署链接
    /appStore/store/contract/invtBillStoreSignPage

    参数说明:
    - docNo: docNo
    """

    url = "/appStore/store/contract/invtBillStoreSignPage"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

import os

from util.client import client

params = {
    "reimbursementType": 0,  # 报销类型
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_invoice_selectCollectionCompany(params=params, headers=headers):
    """
    选择收款单位
    /appStore/store/invoice/selectCollectionCompany

    参数说明:
    - reimbursementType: 报销类型
    """

    url = "/appStore/store/invoice/selectCollectionCompany"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

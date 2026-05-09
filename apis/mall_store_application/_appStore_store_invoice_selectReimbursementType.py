import os

from util.client import client

params = {
    "reimbursementType": 0,  # 报销类型：1：配送费-分公司，2：配送费-总公司，3：服务费-总公司，4：服务费-扬州
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_invoice_selectReimbursementType(params=params, headers=headers):
    """
    报销类型信息查询
    /appStore/store/invoice/selectReimbursementType

    参数说明:
    - reimbursementType: 报销类型：1：配送费-分公司，2：配送费-总公司，3：服务费-总公司，4：服务费-扬州
    """

    url = "/appStore/store/invoice/selectReimbursementType"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

import os

from util.client import client

params = {
    "invoiceType": 0,  # 2：服务费，0：配送费
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_invoice_selectPaymentCompany(params=params, headers=headers):
    """
    selectPaymentCompany
    /appStore/store/invoice/selectPaymentCompany

    参数说明:
    - invoiceType: 2：服务费，0：配送费
    """

    url = "/appStore/store/invoice/selectPaymentCompany"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

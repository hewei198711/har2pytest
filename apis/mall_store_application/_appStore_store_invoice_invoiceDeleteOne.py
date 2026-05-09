import os

from util.client import client

params = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_invoice_invoiceDeleteOne(params=params, headers=headers):
    """
    删除发票--根据主键Id
    /appStore/store/invoice/invoiceDeleteOne

    参数说明:
    - id: id
    """

    url = "/appStore/store/invoice/invoiceDeleteOne"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

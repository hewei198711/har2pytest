import os

from util.client import client

params = {
    "collectionCompanyName": "",  # collectionCompanyName
    "collectionCompanyNo": "",  # collectionCompanyNo
    "totalAmount": "",  # totalAmount
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_invoice_downloadCalculationTable(params=params, headers=headers):
    """
    下载计算表
    /appStore/store/invoice/downloadCalculationTable

    参数说明:
    - collectionCompanyName: collectionCompanyName
    - collectionCompanyNo: collectionCompanyNo
    - totalAmount: totalAmount
    """

    url = "/appStore/store/invoice/downloadCalculationTable"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

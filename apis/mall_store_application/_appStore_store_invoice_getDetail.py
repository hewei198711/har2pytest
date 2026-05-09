import os

from util.client import client

params = {
    "packageId": "",  # packageId
    "pageNum": 0,  # pageNum
    "pageSize": 0,  # pageSize
    "selectReimbursementType": "",  # selectReimbursementType
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_invoice_getDetail(params=params, headers=headers):
    """
    发票采集记录详情
    /appStore/store/invoice/getDetail

    参数说明:
    - packageId: packageId
    - pageNum: pageNum
    - pageSize: pageSize
    - selectReimbursementType: selectReimbursementType
    """

    url = "/appStore/store/invoice/getDetail"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

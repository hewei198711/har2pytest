import os
from urllib.parse import urlencode

from util.client import client

data = {
    "batchId": 0,  # batchId
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_fin_wallet_credit_importBatchDetail(data=data, headers=headers):
    """
    云商信用额录入批次详情列表批量导入
    /mgmt/fin/wallet/credit/importBatchDetail

    参数说明:
    - batchId: batchId
    """

    url = "/mgmt/fin/wallet/credit/importBatchDetail"
    data = urlencode(data)  # application/x-www-form-urlencoded传参需要特殊处理

    with client.post(url=url, data=data, headers=headers) as r:
        return r

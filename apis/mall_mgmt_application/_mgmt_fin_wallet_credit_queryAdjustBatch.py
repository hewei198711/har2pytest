import os
from urllib.parse import urlencode

from util.client import client

data = {
    "id": "",  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_fin_wallet_credit_queryAdjustBatch(data=data, headers=headers):
    """
    信用额调整批次-查询
    /mgmt/fin/wallet/credit/queryAdjustBatch

    参数说明:
    - id: id
    """

    url = "/mgmt/fin/wallet/credit/queryAdjustBatch"
    data = urlencode(data)  # application/x-www-form-urlencoded传参需要特殊处理

    with client.post(url=url, data=data, headers=headers) as r:
        return r

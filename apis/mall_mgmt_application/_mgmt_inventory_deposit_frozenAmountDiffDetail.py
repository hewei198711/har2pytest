import os

from util.client import client

params = {
    "month": 0,  # month
    "storeCode": "",  # storeCode
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_deposit_frozenAmountDiffDetail(params=params, headers=headers):
    """
    签约专用款(差额)详情查看
    /mgmt/inventory/deposit/frozenAmountDiffDetail

    参数说明:
    - month: month
    - storeCode: storeCode
    """

    url = "/mgmt/inventory/deposit/frozenAmountDiffDetail"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

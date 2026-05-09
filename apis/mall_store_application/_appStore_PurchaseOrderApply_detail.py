import os

from util.client import client

params = {
    "applyId": 0,  # 申请id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _appStore_PurchaseOrderApply_detail(params=params, headers=headers):
    """
    详情修改申请
    /appStore/PurchaseOrderApply/detail

    参数说明:
    - applyId: 申请id
    """

    url = "/appStore/PurchaseOrderApply/detail"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

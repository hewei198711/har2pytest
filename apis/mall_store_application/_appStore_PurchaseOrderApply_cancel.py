import os

from util.client import client

data = {
    "applyId": 0,  # 申请id
    "storeCode": "",  # 服务中心编号,不需填写
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _appStore_PurchaseOrderApply_cancel(data=data, headers=headers):
    """
    取消修改申请
    /appStore/PurchaseOrderApply/cancel

    参数说明:
    - applyId: 申请id
    - storeCode: 服务中心编号,不需填写
    """

    url = "/appStore/PurchaseOrderApply/cancel"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

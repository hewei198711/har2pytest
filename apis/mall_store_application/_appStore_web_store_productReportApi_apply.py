import os

from util.client import client

data = {
    "applyCredential": "",  # 申请凭证 多个的话,号分开
    "applyReason": "",  # 申请原因
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_web_store_productReportApi_apply(data=data, headers=headers):
    """
    成品报告申请
    /appStore/web/store/productReportApi/apply

    参数说明:
    - applyCredential: 申请凭证 多个的话,号分开
    - applyReason: 申请原因
    """

    url = "/appStore/web/store/productReportApi/apply"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

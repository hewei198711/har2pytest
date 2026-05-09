import os

from util.client import client

params = {
    "returnNo": "",  # returnNo
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_mobile_orderReturn_preAudit(params=params, headers=headers):
    """
    服务中心退货审核前检查
    /appStore/mobile/orderReturn/preAudit

    参数说明:
    - returnNo: returnNo
    """

    url = "/appStore/mobile/orderReturn/preAudit"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

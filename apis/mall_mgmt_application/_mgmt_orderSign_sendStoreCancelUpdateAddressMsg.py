import os

from util.client import client

params = {
    "storeCode": "",  # 服务中心编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_orderSign_sendStoreCancelUpdateAddressMsg(params=params, headers=headers):
    """
    批量发送结点信息功能 站内信,短信
    /mgmt/orderSign/sendStoreCancelUpdateAddressMsg

    参数说明:
    - storeCode: 服务中心编号
    """

    url = "/mgmt/orderSign/sendStoreCancelUpdateAddressMsg"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

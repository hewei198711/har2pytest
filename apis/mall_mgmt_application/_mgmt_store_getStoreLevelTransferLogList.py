import os

from util.client import client

params = {
    "storeCode": "",  # 服务中心编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_getStoreLevelTransferLogList(params=params, headers=headers):
    """
    获取服务中心等级标识转让取消列表
    /mgmt/store/getStoreLevelTransferLogList

    参数说明:
    - storeCode: 服务中心编号
    """

    url = "/mgmt/store/getStoreLevelTransferLogList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

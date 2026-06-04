import os

from util.client import client

params = {
    "pageNum": 0,  # 页码
    "pageSize": 0,  # 页大小
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_getStoreContractNotifySettingList(params=params, headers=headers):
    """
    查询电子合同消息推送设置列表
    /mgmt/store/getStoreContractNotifySettingList

    参数说明:
    - pageNum: 页码
    - pageSize: 页大小
    """

    url = "/mgmt/store/getStoreContractNotifySettingList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

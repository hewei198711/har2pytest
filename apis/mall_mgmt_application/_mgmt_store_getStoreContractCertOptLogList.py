import os

from util.client import client

params = {
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 每页显示数
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_getStoreContractCertOptLogList(params=params, headers=headers):
    """
    获取电子合同认证信息操作记录
    /mgmt/store/getStoreContractCertOptLogList

    参数说明:
    - pageNum: 页数
    - pageSize: 每页显示数
    """

    url = "/mgmt/store/getStoreContractCertOptLogList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

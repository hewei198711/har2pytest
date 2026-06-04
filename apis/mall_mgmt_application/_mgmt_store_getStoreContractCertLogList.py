import os

from util.client import client

params = {
    "customerNo": "",  # 服务中心编号/服务公司编号
    "pageNum": 0,  # 页码
    "pageSize": 0,  # 每页页数
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_getStoreContractCertLogList(params=params, headers=headers):
    """
    电子印章认证信息历史记录列表
    /mgmt/store/getStoreContractCertLogList

    参数说明:
    - customerNo: 服务中心编号/服务公司编号
    - pageNum: 页码
    - pageSize: 每页页数
    """

    url = "/mgmt/store/getStoreContractCertLogList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

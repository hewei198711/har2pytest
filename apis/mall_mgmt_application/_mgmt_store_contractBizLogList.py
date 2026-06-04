import os

from util.client import client

params = {
    "customerType": 0,  # 客户类型，1/服务中心，2/服务公司
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 每页显示数
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_contractBizLogList(params=params, headers=headers):
    """
    获取经营合同变更日志列表
    /mgmt/store/contractBizLogList

    参数说明:
    - customerType: 客户类型，1/服务中心，2/服务公司
    - pageNum: 页数
    - pageSize: 每页显示数
    """

    url = "/mgmt/store/contractBizLogList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

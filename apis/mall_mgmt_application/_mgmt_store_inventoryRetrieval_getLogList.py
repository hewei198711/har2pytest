import os

from util.client import client

params = {
    "endOperateTime": "",  # 操作结束日期，格式：yyyy-MM-dd
    "operator": "",  # 操作人
    "pageNum": 0,  # pageNum
    "pageSize": 0,  # pageSize
    "startOperateTime": "",  # 操作开始日期，格式：yyyy-MM-dd
    "storeCode": "",  # 服务中心编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_inventoryRetrieval_getLogList(params=params, headers=headers):
    """
    获取库存检索操作日志列表
    /mgmt/store/inventoryRetrieval/getLogList

    参数说明:
    - endOperateTime: 操作结束日期，格式：yyyy-MM-dd
    - operator: 操作人
    - pageNum: pageNum
    - pageSize: pageSize
    - startOperateTime: 操作开始日期，格式：yyyy-MM-dd
    - storeCode: 服务中心编号
    """

    url = "/mgmt/store/inventoryRetrieval/getLogList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

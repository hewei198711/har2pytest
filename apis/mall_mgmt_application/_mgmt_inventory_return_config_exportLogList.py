import os

from util.client import client

params = {
    "createEndTime": "",  # 操作结束时间  yyyy-MM-dd
    "createStartTime": "",  # 操作开始时间  yyyy-MM-dd
    "pageNum": 0,  # 第几页
    "pageSize": 0,  # 每页显示页数
    "storeCode": "",  # 服务中心编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_return_config_exportLogList(params=params, headers=headers):
    """
    导出操作记录列表
    /mgmt/inventory/return/config/exportLogList

    参数说明:
    - createEndTime: 操作结束时间  yyyy-MM-dd
    - createStartTime: 操作开始时间  yyyy-MM-dd
    - pageNum: 第几页
    - pageSize: 每页显示页数
    - storeCode: 服务中心编号
    """

    url = "/mgmt/inventory/return/config/exportLogList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

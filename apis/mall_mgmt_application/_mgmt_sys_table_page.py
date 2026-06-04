import os

from util.client import client

params = {
    "channel": [],  # 渠道 1:服务中心,2:商城,3:服务中心+商城
    "pageNum": 0,  # 当前页
    "pageSize": 0,  # 页码
    "status": 0,  # 表格状态:1->启用,0:禁用
    "tableName": "",  # 表格名称
    "typeId": 0,  # 表格类型id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_table_page(params=params, headers=headers):
    """
    查询表格列表
    /mgmt/sys/table/page

    参数说明:
    - channel: 渠道 1:服务中心,2:商城,3:服务中心+商城
    - pageNum: 当前页
    - pageSize: 页码
    - status: 表格状态:1->启用,0:禁用
    - tableName: 表格名称
    - typeId: 表格类型id
    """

    url = "/mgmt/sys/table/page"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

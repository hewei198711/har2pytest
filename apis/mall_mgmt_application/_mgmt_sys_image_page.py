import os

from util.client import client

params = {
    "channel": 0,  # 渠道 1:服务中心,2:微店,3:服务中心+微店
    "manualName": "",  # 形象手册名称
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 页大小
    "status": 0,  # 使用状态:1->启用,0:禁用
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_image_page(params=params, headers=headers):
    """
    查询形象手册列表
    /mgmt/sys/image/page

    参数说明:
    - channel: 渠道 1:服务中心,2:微店,3:服务中心+微店
    - manualName: 形象手册名称
    - pageNum: 页数
    - pageSize: 页大小
    - status: 使用状态:1->启用,0:禁用
    """

    url = "/mgmt/sys/image/page"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

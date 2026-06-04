import os

from util.client import client

params = {
    "businessRange": 0,  # 业务范围
    "depotCode": "",  # 仓库编码
    "pageNum": 0,  # 当前页
    "pageSize": 0,  # 每页大小
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_depot_page(params=params, headers=headers):
    """
    翻页查询仓库信息
    /mgmt/sys/depot/page

    参数说明:
    - businessRange: 业务范围
    - depotCode: 仓库编码
    - pageNum: 当前页
    - pageSize: 每页大小
    """

    url = "/mgmt/sys/depot/page"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

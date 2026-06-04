import os

from util.client import client

params = {
    "pageNum": 0,  # 当前页
    "pageSize": 0,  # 页码
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_table_type_page(params=params, headers=headers):
    """
    分页获取表格类型
    /mgmt/sys/table/type/page

    参数说明:
    - pageNum: 当前页
    - pageSize: 页码
    """

    url = "/mgmt/sys/table/type/page"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

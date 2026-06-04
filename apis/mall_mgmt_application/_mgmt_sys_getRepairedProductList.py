import os

from util.client import client

params = {
    "pageNum": "",  # 当前页码,默认为1
    "pageSize": "",  # 当前显示的条数（默认为0不分页，显示全部查询结果,需要分页请传非零的正整数）
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_getRepairedProductList(params=params, headers=headers):
    """
    获取可维修的商品列表
    /mgmt/sys/getRepairedProductList

    参数说明:
    - pageNum: 当前页码,默认为1
    - pageSize: 当前显示的条数（默认为0不分页，显示全部查询结果,需要分页请传非零的正整数）
    """

    url = "/mgmt/sys/getRepairedProductList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

import os

from util.client import client

params = {
    "fittingSerialno": "",  # 配件编码
    "fittingTitle": "",  # 配件名称
    "pageNum": "",  # 当前页码,默认为1
    "pageSize": "",  # 当前显示的条数,默认为10
    "productSerialno": "",  # 产品编码
    "productTitle": "",  # 产品名称
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_getFittingPages(params=params, headers=headers):
    """
    获取配件分页信息
    /mgmt/sys/getFittingPages

    参数说明:
    - fittingSerialno: 配件编码
    - fittingTitle: 配件名称
    - pageNum: 当前页码,默认为1
    - pageSize: 当前显示的条数,默认为10
    - productSerialno: 产品编码
    - productTitle: 产品名称
    """

    url = "/mgmt/sys/getFittingPages"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

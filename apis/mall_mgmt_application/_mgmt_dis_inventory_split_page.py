import os

from util.client import client

data = {
    "beginTime": "",  # 停止时间
    "endTime": "",  # 停止时间
    "pageNum": 0,  # TODO: 添加参数说明
    "pageSize": 0,  # TODO: 添加参数说明
    "product": "",  # 套装产品编码/名称
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_dis_inventory_split_page(data=data, headers=headers):
    """
    查询套装拆分列表
    /mgmt/dis-inventory/split/page

    参数说明:
    - beginTime: 停止时间
    - endTime: 停止时间
    - product: 套装产品编码/名称
    """

    url = "/mgmt/dis-inventory/split/page"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

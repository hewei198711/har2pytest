import os

from util.client import client

data = {
    "combineIds": [],  # TODO: 添加参数说明
    "pageNum": 0,  # TODO: 添加参数说明
    "pageSize": 0,  # TODO: 添加参数说明
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_dis_inventory_combine_detail(data=data, headers=headers):
    """
    分页查询套装组合明细
    /mgmt/dis-inventory/combine/detail
    """

    url = "/mgmt/dis-inventory/combine/detail"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

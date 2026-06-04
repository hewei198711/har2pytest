import os

from util.client import client

data = {
    "pageNum": 0,  # TODO: 添加参数说明
    "pageSize": 0,  # TODO: 添加参数说明
    "productCode": "",  # TODO: 添加参数说明
    "storeCode": "",  # TODO: 添加参数说明
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_dis_inventory_split_reverse_page(data=data, headers=headers):
    """
    查询套装保留列表
    /mgmt/dis-inventory/split/reverse/page
    """

    url = "/mgmt/dis-inventory/split/reverse/page"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

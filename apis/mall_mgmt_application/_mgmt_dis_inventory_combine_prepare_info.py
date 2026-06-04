import os

from util.client import client

data = {
    "combineNum": 0,  # TODO: 添加参数说明
    "productCode": "",  # TODO: 添加参数说明
    "storeCode": "",  # TODO: 添加参数说明
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_dis_inventory_combine_prepare_info(data=data, headers=headers):
    """
    获取组合预备信息
    /mgmt/dis-inventory/combine/prepare-info
    """

    url = "/mgmt/dis-inventory/combine/prepare-info"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

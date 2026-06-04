import os

from util.client import client

data = {
    "combines": [{"combineNum": 0, "productCode": "", "storeCode": ""}],  # TODO: 添加参数说明
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_dis_inventory_combine_preview(data=data, headers=headers):
    """
    套装组合预览
    /mgmt/dis-inventory/combine/preview
    """

    url = "/mgmt/dis-inventory/combine/preview"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

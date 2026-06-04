import os

from util.client import client

data = {
    "fittingPrice": 0.0,  # 配件价格
    "fittingSerialno": "",  # 配件编码
    "fittingTitle": "",  # 配件名称
    "id": 0,  # 主键
    "productSerialno": "",  # 产品编码
    "productTitle": "",  # 产品名称
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_addFitting(data=data, headers=headers):
    """
    新增配件
    /mgmt/sys/addFitting

    参数说明:
    - fittingPrice: 配件价格
    - fittingSerialno: 配件编码
    - fittingTitle: 配件名称
    - id: 主键
    - productSerialno: 产品编码
    - productTitle: 产品名称
    """

    url = "/mgmt/sys/addFitting"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

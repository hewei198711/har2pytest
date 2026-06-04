import os
from urllib.parse import urlencode

from util.client import client

data = {
    "id": "",  # 主产品池商品主键id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_prmt_combine_deleteProduct(data=data, headers=headers):
    """
    详情页删除主产品池商品
    /mgmt/prmt/combine/deleteProduct

    参数说明:
    - id: 主产品池商品主键id
    """

    url = "/mgmt/prmt/combine/deleteProduct"
    data = urlencode(data)  # application/x-www-form-urlencoded传参需要特殊处理

    with client.post(url=url, data=data, headers=headers) as r:
        return r

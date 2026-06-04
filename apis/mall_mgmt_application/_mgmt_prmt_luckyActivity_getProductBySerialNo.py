import os

from util.client import client

data = {
    "id": 0,  # 活动id
    "importKey": "",  # 导入/新增 操作键
    "serialNo": "",  # 主产品编码
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_luckyActivity_getProductBySerialNo(data=data, headers=headers):
    """
    根据商品编码精确查询商品
    /mgmt/prmt/luckyActivity/getProductBySerialNo

    参数说明:
    - id: 活动id
    - importKey: 导入/新增 操作键
    - serialNo: 主产品编码
    """

    url = "/mgmt/prmt/luckyActivity/getProductBySerialNo"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

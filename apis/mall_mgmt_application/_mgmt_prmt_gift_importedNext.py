import os

from util.client import client

data = {
    "importKey": "",  # 导入操作键
    "promotionCode": "",  # 活动编号
    "promotionName": "",  # 活动名称
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_gift_importedNext(data=data, headers=headers):
    """
    导入文件后下一步操作校验
    /mgmt/prmt/gift/importedNext

    参数说明:
    - importKey: 导入操作键
    - promotionCode: 活动编号
    - promotionName: 活动名称
    """

    url = "/mgmt/prmt/gift/importedNext"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

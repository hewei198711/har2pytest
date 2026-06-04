import os

from util.client import client

data = {
    "relationList": [{"fileUrl": "", "originalFilename": ""}],  # 文件关系列表
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_importOfflineContracts(data=data, headers=headers):
    """
    导入线下合同
    /mgmt/store/importOfflineContracts

    参数说明:
    - relationList: 文件关系列表
    - relationList.fileUrl: 现文件链接
    - relationList.originalFilename: 原文件名
    """

    url = "/mgmt/store/importOfflineContracts"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

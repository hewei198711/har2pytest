import os

from util.client import client

data = {
    "downloader": "",  # 下载者
    "id": 0,  # 主键id
    "storeCode": "",  # 服务中心编码
    "storeName": "",  # 服务中心名称
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_image_record_save(data=data, headers=headers):
    """
    保存形象手册下载记录
    /mgmt/sys/image/record/save

    参数说明:
    - downloader: 下载者
    - id: 主键id
    - storeCode: 服务中心编码
    - storeName: 服务中心名称
    """

    url = "/mgmt/sys/image/record/save"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

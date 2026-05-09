import os

from util.client import client

params = {
    "id": 0,  # id
    "nos": [],  # nos
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_web_store_productReportApi_download(params=params, headers=headers):
    """
    下载成品报告(失败的话返回权限已过期4)
    /appStore/web/store/productReportApi/download

    参数说明:
    - id: id
    - nos: nos
    """

    url = "/appStore/web/store/productReportApi/download"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

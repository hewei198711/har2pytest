import os

from util.client import client

data = {
    "id": 0,  # id
    "sort": 0,  # 排序
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_updatePopUpSortById(data=data, headers=headers):
    """
    按id更新弹窗排序值
    /mgmt/cms/updatePopUpSortById

    参数说明:
    - id: id
    - sort: 排序
    """

    url = "/mgmt/cms/updatePopUpSortById"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

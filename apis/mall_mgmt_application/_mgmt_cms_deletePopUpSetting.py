import os

from util.client import client

data = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_cms_deletePopUpSetting(data=data, headers=headers):
    """
    删除指定id的弹窗配置
    /mgmt/cms/deletePopUpSetting

    参数说明:
    - id: id
    """

    url = "/mgmt/cms/deletePopUpSetting"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

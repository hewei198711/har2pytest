import os

from util.client import client

data = {
    "id": 0,  # 第三方软件推广链接id
    "useStatus": 0,  # 启用状态: 1:启用 0:禁用
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_promotionLink_changUseStatus(data=data, headers=headers):
    """
    修改指定id的第三方软件推广链接的启用禁用状态
    /mgmt/cms/promotionLink/changUseStatus

    参数说明:
    - id: 第三方软件推广链接id
    - useStatus: 启用状态: 1:启用 0:禁用
    """

    url = "/mgmt/cms/promotionLink/changUseStatus"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

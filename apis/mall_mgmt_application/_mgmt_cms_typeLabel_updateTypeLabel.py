import os

from util.client import client

data = {
    "iconUrl": "",  # 分类图标链接
    "id": 0,  # 标签ID
    "name": "",  # 标签名称
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_typeLabel_updateTypeLabel(data=data, headers=headers):
    """
    修改类型标签
    /mgmt/cms/typeLabel/updateTypeLabel

    参数说明:
    - iconUrl: 分类图标链接
    - id: 标签ID
    - name: 标签名称
    """

    url = "/mgmt/cms/typeLabel/updateTypeLabel"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

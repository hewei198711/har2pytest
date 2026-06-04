import os

from util.client import client

data = {
    "iconUrl": "",  # 分类图标链接
    "id": 0,  # 标签ID
    "name": "",  # 标签名称
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_cms_classificationLabel_updateLabel(data=data, headers=headers):
    """
    修改分类标签
    /mgmt/cms/classificationLabel/updateLabel

    参数说明:
    - iconUrl: 分类图标链接
    - id: 标签ID
    - name: 标签名称
    """

    url = "/mgmt/cms/classificationLabel/updateLabel"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

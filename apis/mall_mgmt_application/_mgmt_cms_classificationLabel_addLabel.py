import os

from util.client import client

data = {
    "iconUrl": "",  # 分类图标链接
    "name": "",  # 标签名称
    "parentId": 0,  # 父级分类id(一级分类为0)
    "type": 0,  # 归属类型 1：素材 2：文档
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_cms_classificationLabel_addLabel(data=data, headers=headers):
    """
    添加分类标签
    /mgmt/cms/classificationLabel/addLabel

    参数说明:
    - iconUrl: 分类图标链接
    - name: 标签名称
    - parentId: 父级分类id(一级分类为0)
    - type: 归属类型 1：素材 2：文档
    """

    url = "/mgmt/cms/classificationLabel/addLabel"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

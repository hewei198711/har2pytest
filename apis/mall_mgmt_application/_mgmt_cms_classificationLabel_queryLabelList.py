import os

from util.client import client

data = {
    "type": 0,  # 归属类型 1：素材 2：文档
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_cms_classificationLabel_queryLabelList(data=data, headers=headers):
    """
    查询分类标签列表
    /mgmt/cms/classificationLabel/queryLabelList

    参数说明:
    - type: 归属类型 1：素材 2：文档
    """

    url = "/mgmt/cms/classificationLabel/queryLabelList"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

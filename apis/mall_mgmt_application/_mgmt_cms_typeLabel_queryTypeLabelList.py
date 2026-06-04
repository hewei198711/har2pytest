import os

from util.client import client

data = {
    "type": 0,  # 归属类型 1：素材 2：文档
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_typeLabel_queryTypeLabelList(data=data, headers=headers):
    """
    查询类型标签列表
    /mgmt/cms/typeLabel/queryTypeLabelList

    参数说明:
    - type: 归属类型 1：素材 2：文档
    """

    url = "/mgmt/cms/typeLabel/queryTypeLabelList"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

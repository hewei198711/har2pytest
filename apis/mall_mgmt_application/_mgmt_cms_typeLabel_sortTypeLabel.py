import os

from util.client import client

data = {
    "cmsLabelUpdateBatchReqVOS": [{"id": 0, "sort": 0}],  # 标签ID
    "type": 0,  # 归属类型 1：素材 2：文档
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_typeLabel_sortTypeLabel(data=data, headers=headers):
    """
    排序
    /mgmt/cms/typeLabel/sortTypeLabel

    参数说明:
    - cmsLabelUpdateBatchReqVOS: 标签ID
    - cmsLabelUpdateBatchReqVOS.id: 标签ID
    - cmsLabelUpdateBatchReqVOS.sort: 排序
    - type: 归属类型 1：素材 2：文档
    """

    url = "/mgmt/cms/typeLabel/sortTypeLabel"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

import os

from util.client import client

data = {
    "classificationLabelIds": "",  # 分类标签ID,多个ID以逗号隔开,例：1,2,3
    "materialIdList": [],  # 素材id列表
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_material_batchUpdateMaterialClassification(data=data, headers=headers):
    """
    批量修改素材标签
    /mgmt/cms/material/batchUpdateMaterialClassification

    参数说明:
    - classificationLabelIds: 分类标签ID,多个ID以逗号隔开,例：1,2,3
    - materialIdList: 素材id列表
    """

    url = "/mgmt/cms/material/batchUpdateMaterialClassification"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

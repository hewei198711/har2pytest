import os

from util.client import client

data = {
    "materialIdList": [],  # 素材id列表
    "secondTypeLabelId": 0,  # 素材二级分类id
    "typeLabelId": 0,  # 素材一级分类id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_material_batchUpdateMaterialType(data=data, headers=headers):
    """
    批量修改素材分类
    /mgmt/cms/material/batchUpdateMaterialType

    参数说明:
    - materialIdList: 素材id列表
    - secondTypeLabelId: 素材二级分类id
    - typeLabelId: 素材一级分类id
    """

    url = "/mgmt/cms/material/batchUpdateMaterialType"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

import os

from util.client import client

data = {
    "editType": 0,  # 修改产品池类型: 0-赠品池名称 1-主商品池名称 2-主商品池说明
    "id": 0,  # 活动id
    "productGroupIndex": 0,  # 主产品池序号(修改赠品池时不需携带此属性)
    "productGroupName": "",  # 主产品池名称
    "productGroupRemark": "",  # 主产品池说明
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_combine_editProductGroupName(data=data, headers=headers):
    """
    修改主(赠)商品池名称
    /mgmt/prmt/combine/editProductGroupName

    参数说明:
    - editType: 修改产品池类型: 0-赠品池名称 1-主商品池名称 2-主商品池说明
    - id: 活动id
    - productGroupIndex: 主产品池序号(修改赠品池时不需携带此属性)
    - productGroupName: 主产品池名称
    - productGroupRemark: 主产品池说明
    """

    url = "/mgmt/prmt/combine/editProductGroupName"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

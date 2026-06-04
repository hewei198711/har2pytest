import os

from util.client import client

params = {
    "id": "",  # 活动id
    "moduleId": "",  # 模块id
    "serialNo": "",  # 商品编码
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_welfare_selectProductFromPromotionInfo(params=params, headers=headers):
    """
    详情页模糊查询活动商品
    /mgmt/prmt/welfare/selectProductFromPromotionInfo

    参数说明:
    - id: 活动id
    - moduleId: 模块id
    - serialNo: 商品编码
    """

    url = "/mgmt/prmt/welfare/selectProductFromPromotionInfo"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

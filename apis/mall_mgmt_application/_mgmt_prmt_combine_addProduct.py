import os

from util.client import client

data = {
    "limitNum": 0,  # 最大购买数量
    "openSelect": False,  # 是否开启前端搜索: false-否 true-是
    "productGroupIndex": 0,  # 主产品池序号
    "productGroupName": "",  # 主产品池名称
    "productGroupRemark": "",  # 主产品池说明
    "promotionId": 0,  # 活动id
    "serialNo": "",  # 商品编码
    "sort": 0,  # 排序
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_combine_addProduct(data=data, headers=headers):
    """
    详情页添加主产品池商品
    /mgmt/prmt/combine/addProduct

    参数说明:
    - limitNum: 最大购买数量
    - openSelect: 是否开启前端搜索: false-否 true-是
    - productGroupIndex: 主产品池序号
    - productGroupName: 主产品池名称
    - productGroupRemark: 主产品池说明
    - promotionId: 活动id
    - serialNo: 商品编码
    - sort: 排序
    """

    url = "/mgmt/prmt/combine/addProduct"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

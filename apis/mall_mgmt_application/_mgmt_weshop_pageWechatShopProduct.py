import os

from util.client import client

data = {
    "from": 0,  # TODO: 添加参数说明
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 每页显示数
    "serialNo": "",  # 商品编码
    "title": "",  # 商品名称
    "transferType": 0,  # 状态：1-未转分，2-部分转分，3-全部转分
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_weshop_pageWechatShopProduct(data=data, headers=headers):
    """
    分页查询微信小店转分列表
    /mgmt/weshop/pageWechatShopProduct

    参数说明:
    - pageNum: 页数
    - pageSize: 每页显示数
    - serialNo: 商品编码
    - title: 商品名称
    - transferType: 状态：1-未转分，2-部分转分，3-全部转分
    """

    url = "/mgmt/weshop/pageWechatShopProduct"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

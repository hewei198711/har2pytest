import os

from util.client import client

data = {
    "from": 0,  # TODO: 添加参数说明
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 每页显示数
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_weshop_getWechatShopOrderConfigLog(data=data, headers=headers):
    """
    订单超时设置-微信小店修改记录
    /mgmt/weshop/getWechatShopOrderConfigLog

    参数说明:
    - pageNum: 页数
    - pageSize: 每页显示数
    """

    url = "/mgmt/weshop/getWechatShopOrderConfigLog"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

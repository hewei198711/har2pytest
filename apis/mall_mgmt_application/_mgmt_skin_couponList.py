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


def _mgmt_skin_couponList(data=data, headers=headers):
    """
    优惠券列表
    /mgmt/skin/couponList

    参数说明:
    - pageNum: 页数
    - pageSize: 每页显示数
    """

    url = "/mgmt/skin/couponList"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

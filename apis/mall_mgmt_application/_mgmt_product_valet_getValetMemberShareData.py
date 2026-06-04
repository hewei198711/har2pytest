import os

from util.client import client

data = {
    "memberId": "",  # 会员id
    "pageNum": 0,  # 页码
    "pageSize": 0,  # 页面大小
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_product_valet_getValetMemberShareData(data=data, headers=headers):
    """
    代客选品数据-会员分享数据
    /mgmt/product/valet/getValetMemberShareData

    参数说明:
    - memberId: 会员id
    - pageNum: 页码
    - pageSize: 页面大小
    """

    url = "/mgmt/product/valet/getValetMemberShareData"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

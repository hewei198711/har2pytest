import os

from util.client import client

data = {
    "memberCard": "",  # 会员卡号
    "memberPhone": "",  # 会员手机号
    "memberType": 0,  # 会员类别：1->普通顾客；2->优惠顾客；3->云商；4->微店（云+）
    "pageNum": 0,  # 页码
    "pageSize": 0,  # 页面大小
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_product_valet_getValetMemberList(data=data, headers=headers):
    """
    代客选品数据-会员列表
    /mgmt/product/valet/getValetMemberList

    参数说明:
    - memberCard: 会员卡号
    - memberPhone: 会员手机号
    - memberType: 会员类别：1->普通顾客；2->优惠顾客；3->云商；4->微店（云+）
    - pageNum: 页码
    - pageSize: 页面大小
    """

    url = "/mgmt/product/valet/getValetMemberList"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

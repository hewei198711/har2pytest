import os

from util.client import client

data = {
    "cardNo": "",  # 会员卡号
    "memberType": 0,  # 顾客类型 1->普通顾客；2->优惠顾客；3->云商；4->微店（云+）
    "mobile": "",  # 手机号码
    "name": "",  # 姓名
    "pageNum": 0,  # 页码
    "pageSize": 0,  # 每页页数
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_whiteList_queryWhiteListUserList(data=data, headers=headers):
    """
    获取白名单用户列表
    /mgmt/cms/whiteList/queryWhiteListUserList

    参数说明:
    - cardNo: 会员卡号
    - memberType: 顾客类型 1->普通顾客；2->优惠顾客；3->云商；4->微店（云+）
    - mobile: 手机号码
    - name: 姓名
    - pageNum: 页码
    - pageSize: 每页页数
    """

    url = "/mgmt/cms/whiteList/queryWhiteListUserList"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

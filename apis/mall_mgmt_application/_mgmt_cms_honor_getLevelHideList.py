import os

from util.client import client

data = {
    "cardNo": "",  # 会员卡号
    "mobile": "",  # 注册手机号
    "pageNum": 0,  # 页码
    "pageSize": 0,  # 每页页数
    "userName": "",  # 姓名
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_honor_getLevelHideList(data=data, headers=headers):
    """
    获取用户荣誉(会员等级隐藏)名单
    /mgmt/cms/honor/getLevelHideList

    参数说明:
    - cardNo: 会员卡号
    - mobile: 注册手机号
    - pageNum: 页码
    - pageSize: 每页页数
    - userName: 姓名
    """

    url = "/mgmt/cms/honor/getLevelHideList"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

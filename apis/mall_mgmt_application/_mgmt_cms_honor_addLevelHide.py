import os

from util.client import client

data = {
    "cardNo": "",  # 用户卡号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_honor_addLevelHide(data=data, headers=headers):
    """
    新增用户荣誉(会员等级隐藏)名单
    /mgmt/cms/honor/addLevelHide

    参数说明:
    - cardNo: 用户卡号
    """

    url = "/mgmt/cms/honor/addLevelHide"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

import os

from util.client import client

params = {
    "cardNo": "",  # 会员卡号
    "memberType": "",  # 顾客类型: 1.会员 2.VIP会员 3.云商 4.微店
    "mobile": "",  # 手机号码
    "name": "",  # 姓名
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_whiteList_exportWhiteListUsers(params=params, headers=headers):
    """
    导出白名单用户列表
    /mgmt/cms/whiteList/exportWhiteListUsers

    参数说明:
    - cardNo: 会员卡号
    - memberType: 顾客类型: 1.会员 2.VIP会员 3.云商 4.微店
    - mobile: 手机号码
    - name: 姓名
    """

    url = "/mgmt/cms/whiteList/exportWhiteListUsers"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

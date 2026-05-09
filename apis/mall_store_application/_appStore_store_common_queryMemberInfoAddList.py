import os

from util.client import client

params = {
    "cardNo": "",  # 会员卡号
    "from": 0,  # TODO: 添加参数说明
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 每页显示数
    "realname": "",  # 会员姓名
    "storeCode": "",  # 最大购货店
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_common_queryMemberInfoAddList(params=params, headers=headers):
    """
    查询补充会员信息资料列表
    /appStore/store/common/queryMemberInfoAddList

    参数说明:
    - cardNo: 会员卡号
    - pageNum: 页数
    - pageSize: 每页显示数
    - realname: 会员姓名
    - storeCode: 最大购货店
    """

    url = "/appStore/store/common/queryMemberInfoAddList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

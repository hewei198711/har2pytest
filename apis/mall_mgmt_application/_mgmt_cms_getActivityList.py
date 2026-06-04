import os

from util.client import client

params = {
    "pageNum": 0,  # 页码
    "pageSize": 0,  # 每页页数
    "promotionCode": "",  # 关联的活动编码
    "promotionName": "",  # 活动名称
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_getActivityList(params=params, headers=headers):
    """
    获取活动列表（点击关联活动）
    /mgmt/cms/getActivityList

    参数说明:
    - pageNum: 页码
    - pageSize: 每页页数
    - promotionCode: 关联的活动编码
    - promotionName: 活动名称
    """

    url = "/mgmt/cms/getActivityList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

import os

from util.client import client

data = {
    "displayUserSerial": "",  # 展示用户关联序列号
    "pageNum": 0,  # 页码
    "pageSize": 0,  # 每页页数
    "relateType": 0,  # 关联类型:1.素材;2.问卷;3.直播间;
    "searchCriteria": "",  # 搜索条件
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_displayUser_queryDisplayUserList(data=data, headers=headers):
    """
    获取展示用户列表
    /mgmt/cms/displayUser/queryDisplayUserList

    参数说明:
    - displayUserSerial: 展示用户关联序列号
    - pageNum: 页码
    - pageSize: 每页页数
    - relateType: 关联类型:1.素材;2.问卷;3.直播间;
    - searchCriteria: 搜索条件
    """

    url = "/mgmt/cms/displayUser/queryDisplayUserList"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

import os

from util.client import client

data = {
    "dataDate": "",  # 数据时间 格式yyyy-MM-dd 时间段用逗号分隔
    "homePageId": 0,  # 首页id
    "location": 0,  # 平台: 2.APP 3.小程序
    "pageNum": 0,  # TODO: 添加参数说明
    "pageSize": 0,  # TODO: 添加参数说明
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_dataAdmin_magicHomePage_getSumStatistics(data=data, headers=headers):
    """
    查询魔法首页总体统计数据
    /mgmt/dataAdmin/magicHomePage/getSumStatistics

    参数说明:
    - dataDate: 数据时间 格式yyyy-MM-dd 时间段用逗号分隔
    - homePageId: 首页id
    - location: 平台: 2.APP 3.小程序
    """

    url = "/mgmt/dataAdmin/magicHomePage/getSumStatistics"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

import os

from util.client import client

data = {
    "channel": "",  # 渠道
    "searchTime": "",  # 查询时间
    "searchType": "",  # 查询类型:1.按月查询 2.按日查询
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_dataAdmin_page_statistics_getBrowsePathList(data=data, headers=headers):
    """
    顾客浏览路径
    /mgmt/dataAdmin/page/statistics/getBrowsePathList

    参数说明:
    - channel: 渠道
    - searchTime: 查询时间
    - searchType: 查询类型:1.按月查询 2.按日查询
    """

    url = "/mgmt/dataAdmin/page/statistics/getBrowsePathList"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

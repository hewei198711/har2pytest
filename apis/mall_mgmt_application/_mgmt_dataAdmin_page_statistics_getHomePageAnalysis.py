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


def _mgmt_dataAdmin_page_statistics_getHomePageAnalysis(data=data, headers=headers):
    """
    埋点数据-首页数据
    /mgmt/dataAdmin/page/statistics/getHomePageAnalysis

    参数说明:
    - channel: 渠道
    - searchTime: 查询时间
    - searchType: 查询类型:1.按月查询 2.按日查询
    """

    url = "/mgmt/dataAdmin/page/statistics/getHomePageAnalysis"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

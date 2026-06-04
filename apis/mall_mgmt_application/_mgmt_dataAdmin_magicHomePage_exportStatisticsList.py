import os

from util.client import client

params = {
    "dataDate": "",  # dataDate
    "homePageId": 0,  # homePageId
    "location": 0,  # location
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_dataAdmin_magicHomePage_exportStatisticsList(params=params, headers=headers):
    """
    导出魔法首页统计数据列表
    /mgmt/dataAdmin/magicHomePage/exportStatisticsList

    参数说明:
    - dataDate: dataDate
    - homePageId: homePageId
    - location: location
    """

    url = "/mgmt/dataAdmin/magicHomePage/exportStatisticsList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

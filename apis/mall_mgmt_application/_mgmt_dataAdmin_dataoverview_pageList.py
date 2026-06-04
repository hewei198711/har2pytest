import os

from util.client import client

data = {
    "endDate": "",  # 结束日期,格式yyyy-MM-dd
    "pageNum": 0,  # TODO: 添加参数说明
    "pageSize": 0,  # TODO: 添加参数说明
    "startDate": "",  # 开始日期,格式yyyy-MM-dd
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_dataAdmin_dataoverview_pageList(data=data, headers=headers):
    """
    查询指定时间区间内数据概览列表
    /mgmt/dataAdmin/dataoverview/pageList

    参数说明:
    - endDate: 结束日期,格式yyyy-MM-dd
    - startDate: 开始日期,格式yyyy-MM-dd
    """

    url = "/mgmt/dataAdmin/dataoverview/pageList"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

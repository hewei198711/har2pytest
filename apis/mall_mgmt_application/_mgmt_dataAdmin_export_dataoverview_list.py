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


def _mgmt_dataAdmin_export_dataoverview_list(data=data, headers=headers):
    """
    数据概览数据明细导出
    /mgmt/dataAdmin/export/dataoverview/list

    参数说明:
    - endDate: 结束日期,格式yyyy-MM-dd
    - startDate: 开始日期,格式yyyy-MM-dd
    """

    url = "/mgmt/dataAdmin/export/dataoverview/list"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

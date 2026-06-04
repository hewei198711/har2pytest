import os

from util.client import client

data = {
    "dateType": 0,  # 时间类型 0:天 ; 1:月 ; 2: 年
    "endTime": "",  # 结束时间
    "pageNum": 0,  # 页码(不传默认为1)
    "pageSize": 0,  # 每页大小(不传默认为10)
    "startTime": "",  # 开始时间
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_dataAdmin_userData_getDayIncreasePage(data=data, headers=headers):
    """
    获取用户增长列表
    /mgmt/dataAdmin/userData/getDayIncreasePage

    参数说明:
    - dateType: 时间类型 0:天 ; 1:月 ; 2: 年
    - endTime: 结束时间
    - pageNum: 页码(不传默认为1)
    - pageSize: 每页大小(不传默认为10)
    - startTime: 开始时间
    """

    url = "/mgmt/dataAdmin/userData/getDayIncreasePage"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

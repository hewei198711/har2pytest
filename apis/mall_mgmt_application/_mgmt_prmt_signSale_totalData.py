import os

from util.client import client

params = {
    "endTime": "",  # 结束时间(yyyy-MM-dd)
    "id": 0,  # 活动id
    "pageNum": 0,  # 当前页
    "pageSize": 0,  # 每页条数
    "startTime": "",  # 开始时间(yyyy-MM-dd)
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_signSale_totalData(params=params, headers=headers):
    """
    累计数据统计
    /mgmt/prmt/signSale/totalData

    参数说明:
    - endTime: 结束时间(yyyy-MM-dd)
    - id: 活动id
    - pageNum: 当前页
    - pageSize: 每页条数
    - startTime: 开始时间(yyyy-MM-dd)
    """

    url = "/mgmt/prmt/signSale/totalData"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

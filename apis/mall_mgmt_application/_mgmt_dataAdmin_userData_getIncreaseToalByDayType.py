import os

from util.client import client

data = {
    "dateType": 0,  # 时间类型 0:天 ; 1:月 ; 2: 年
    "endTime": "",  # 结束时间
    "startTime": "",  # 开始时间
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_dataAdmin_userData_getIncreaseToalByDayType(data=data, headers=headers):
    """
    根据日期类型查询用户增长数
    /mgmt/dataAdmin/userData/getIncreaseToalByDayType

    参数说明:
    - dateType: 时间类型 0:天 ; 1:月 ; 2: 年
    - endTime: 结束时间
    - startTime: 开始时间
    """

    url = "/mgmt/dataAdmin/userData/getIncreaseToalByDayType"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

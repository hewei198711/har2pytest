import os

from util.client import client

data = {
    "customerCard": "",  # 会员卡号
    "endTime": "",  # 管控时间结束
    "pageNum": 0,  # TODO: 添加参数说明
    "pageSize": 0,  # TODO: 添加参数说明
    "registerPhone": "",  # 注册电话
    "startTime": "",  # 管控时间开始
    "warningName": "",  # 预警项目名称
    "warningType": "",  # 预警类型（0：数量；1：PV；2：金额）
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_dataAdmin_export_memberAuthControlRecord(data=data, headers=headers):
    """
    会员权限管控记录列表导出
    /mgmt/dataAdmin/export/memberAuthControlRecord

    参数说明:
    - customerCard: 会员卡号
    - endTime: 管控时间结束
    - registerPhone: 注册电话
    - startTime: 管控时间开始
    - warningName: 预警项目名称
    - warningType: 预警类型（0：数量；1：PV；2：金额）
    """

    url = "/mgmt/dataAdmin/export/memberAuthControlRecord"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

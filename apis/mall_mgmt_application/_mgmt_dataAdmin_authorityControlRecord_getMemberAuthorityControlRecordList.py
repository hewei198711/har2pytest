import os

from util.client import client

params = {
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


def _mgmt_dataAdmin_authorityControlRecord_getMemberAuthorityControlRecordList(params=params, headers=headers):
    """
    获取会员权限控制记录列表
    /mgmt/dataAdmin/authorityControlRecord/getMemberAuthorityControlRecordList

    参数说明:
    - customerCard: 会员卡号
    - endTime: 管控时间结束
    - registerPhone: 注册电话
    - startTime: 管控时间开始
    - warningName: 预警项目名称
    - warningType: 预警类型（0：数量；1：PV；2：金额）
    """

    url = "/mgmt/dataAdmin/authorityControlRecord/getMemberAuthorityControlRecordList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

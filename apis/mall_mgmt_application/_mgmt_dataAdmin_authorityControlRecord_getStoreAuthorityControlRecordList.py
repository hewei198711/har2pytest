import os

from util.client import client

params = {
    "adminCard": "",  # 管理员卡号
    "adminPhone": "",  # 管理员注册电话
    "centerCode": "",  # 服务中心编号
    "centerName": "",  # 服务中心名称
    "endTime": "",  # 管控时间结束
    "pageNum": 0,  # TODO: 添加参数说明
    "pageSize": 0,  # TODO: 添加参数说明
    "startTime": "",  # 管控时间开始
    "warningName": "",  # 预警项目名称
    "warningType": "",  # 预警类型（0：数量；1：PV；2：金额）
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_dataAdmin_authorityControlRecord_getStoreAuthorityControlRecordList(params=params, headers=headers):
    """
    获取店铺权限控制记录列表
    /mgmt/dataAdmin/authorityControlRecord/getStoreAuthorityControlRecordList

    参数说明:
    - adminCard: 管理员卡号
    - adminPhone: 管理员注册电话
    - centerCode: 服务中心编号
    - centerName: 服务中心名称
    - endTime: 管控时间结束
    - startTime: 管控时间开始
    - warningName: 预警项目名称
    - warningType: 预警类型（0：数量；1：PV；2：金额）
    """

    url = "/mgmt/dataAdmin/authorityControlRecord/getStoreAuthorityControlRecordList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

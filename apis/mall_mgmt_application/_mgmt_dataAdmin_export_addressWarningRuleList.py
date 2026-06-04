import os

from util.client import client

data = {
    "endTimeEnd": "",  # 预警结束时间截止
    "endTimeStart": "",  # 预警结束时间起始
    "pageNum": 0,  # TODO: 添加参数说明
    "pageSize": 0,  # TODO: 添加参数说明
    "placeMonth": "",  # 报单月份
    "placeMonthStr": "",  # 报单月份(前端传参)
    "startTimeEnd": "",  # 预警开始时间截止
    "startTimeStart": "",  # 预警开始时间起始
    "status": 0,  # 状态（0：停止，1：启用；2：待审核；3审核不通过）
    "warningName": "",  # 预警名称
    "warningNumber": 0.0,  # 购货人数使用限制
    "warningType": 0,  # 预警方式(0:地址预警；1：电话预警；2：两者都预警)
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_dataAdmin_export_addressWarningRuleList(data=data, headers=headers):
    """
    收货地址预警规则列表导出
    /mgmt/dataAdmin/export/addressWarningRuleList

    参数说明:
    - endTimeEnd: 预警结束时间截止
    - endTimeStart: 预警结束时间起始
    - placeMonth: 报单月份
    - placeMonthStr: 报单月份(前端传参)
    - startTimeEnd: 预警开始时间截止
    - startTimeStart: 预警开始时间起始
    - status: 状态（0：停止，1：启用；2：待审核；3审核不通过）
    - warningName: 预警名称
    - warningNumber: 购货人数使用限制
    - warningType: 预警方式(0:地址预警；1：电话预警；2：两者都预警)
    """

    url = "/mgmt/dataAdmin/export/addressWarningRuleList"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

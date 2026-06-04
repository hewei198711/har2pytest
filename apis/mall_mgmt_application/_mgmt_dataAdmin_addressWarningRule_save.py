import os

from util.client import client

data = {
    "createStaff": "",  # 创建人
    "createTime": "",  # 创建时间
    "endTime": "",  # 预警结束时间
    "remark": "",  # 预警描述
    "ruleId": 0,  # id标识
    "startTime": "",  # 预警开始时间
    "status": 0,  # 状态（0：停止，1：启用；2：待审核；3审核不通过）
    "updateStaff": "",  # 更新账号
    "updateTime": "",  # 更新时间
    "warningGranularity": "",  # 预警粒度
    "warningName": "",  # 预警项目名称
    "warningNumber": 0.0,  # 购货人数使用限制
    "warningType": 0,  # 预警方式(0:地址预警；1：电话预警；2：两者都预警)
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_dataAdmin_addressWarningRule_save(data=data, headers=headers):
    """
    保存预警规则
    /mgmt/dataAdmin/addressWarningRule/save

    参数说明:
    - createStaff: 创建人
    - createTime: 创建时间
    - endTime: 预警结束时间
    - remark: 预警描述
    - ruleId: id标识
    - startTime: 预警开始时间
    - status: 状态（0：停止，1：启用；2：待审核；3审核不通过）
    - updateStaff: 更新账号
    - updateTime: 更新时间
    - warningGranularity: 预警粒度
    - warningName: 预警项目名称
    - warningNumber: 购货人数使用限制
    - warningType: 预警方式(0:地址预警；1：电话预警；2：两者都预警)
    """

    url = "/mgmt/dataAdmin/addressWarningRule/save"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

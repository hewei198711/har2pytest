import os

from util.client import client

data = {
    "authorityNos": [],  # 权限编号集合
    "controlMemberAuthority": "",  # 管控会员权限(0:不管控；1:管控所有；2:管控重点名单)
    "controlStoreAuthority": "",  # 管控门店权限(0:不管控；1:管控所有；2:管控重点名单)
    "createStaff": "",  # 创建人
    "createTime": "",  # 创建时间
    "deliverType": "",  # 交付方式
    "deliverWarningNumber": 0.0,  # 交付预警数量
    "endTime": "",  # 预警结束时间
    "flag": "",  # 执行标识 0：未执行；1：已执行
    "isDeliverWarning": "",  # 是否交付预警（0：否；1：是）
    "isShopWarning": "",  # 是否购货预警（0：否；1：是）
    "orderWay": 0,  # 下单方式(0:所有下单方式；1:自购订单 2:代购订单)
    "productCode": "",  # 产品编号
    "remark": "",  # 预警描述
    "ruleId": 0,  # id标识
    "shopWarningNumber": 0.0,  # 购货预警数量
    "startTime": "",  # 预警开始时间
    "state": "",  # 状态（0：停止，1：启用；2：待审核；3审核不通过）
    "unChooseAllauthority": False,  # 全不勾选权限开关(修改时):true
    "updateStaff": "",  # 更新账号
    "updateTime": "",  # 更新时间
    "warningGranularity": "",  # 预警粒度
    "warningName": "",  # 预警项目名称
    "warningProduct": "",  # 预警产品(0:所有产品；1：单一产品)
    "warningType": "",  # 预警类型（0：数量；1：PV; 2:金额 ）
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_dataAdmin_warningRule_save(data=data, headers=headers):
    """
    数据中心管理后台-预警规则管理-保存预警规则
    /mgmt/dataAdmin/warningRule/save

    参数说明:
    - authorityNos: 权限编号集合
    - controlMemberAuthority: 管控会员权限(0:不管控；1:管控所有；2:管控重点名单)
    - controlStoreAuthority: 管控门店权限(0:不管控；1:管控所有；2:管控重点名单)
    - createStaff: 创建人
    - createTime: 创建时间
    - deliverType: 交付方式
    - deliverWarningNumber: 交付预警数量
    - endTime: 预警结束时间
    - flag: 执行标识 0：未执行；1：已执行
    - isDeliverWarning: 是否交付预警（0：否；1：是）
    - isShopWarning: 是否购货预警（0：否；1：是）
    - orderWay: 下单方式(0:所有下单方式；1:自购订单 2:代购订单)
    - productCode: 产品编号
    - remark: 预警描述
    - ruleId: id标识
    - shopWarningNumber: 购货预警数量
    - startTime: 预警开始时间
    - state: 状态（0：停止，1：启用；2：待审核；3审核不通过）
    - unChooseAllauthority: 全不勾选权限开关(修改时):true
    - updateStaff: 更新账号
    - updateTime: 更新时间
    - warningGranularity: 预警粒度
    - warningName: 预警项目名称
    - warningProduct: 预警产品(0:所有产品；1：单一产品)
    - warningType: 预警类型（0：数量；1：PV; 2:金额 ）
    """

    url = "/mgmt/dataAdmin/warningRule/save"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

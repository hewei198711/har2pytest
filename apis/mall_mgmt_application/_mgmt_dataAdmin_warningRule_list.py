import os

from util.client import client

params = {
    "controlMemberAuthority": "",  # 管控会员权限(0:不管控；1:管控所有；2:管控重点名单)
    "controlStoreAuthority": "",  # 管控门店权限(0:不管控；1:管控所有；2:管控重点名单)
    "deliverType": "",  # 交付方式;目前只有all
    "endTimeEnd": "",  # 预警结束时间截止
    "endTimeStart": "",  # 预警结束时间起始
    "isDeliverWarning": "",  # //是否交付预警 0:否 1：是
    "isShopWarning": "",  # 是否购货预警 0:否 1：是
    "orderWay": 0,  # 下单方式(0:所有下单方式；1:自购订单 2:代购订单)
    "pageNum": 0,  # TODO: 添加参数说明
    "pageSize": 0,  # TODO: 添加参数说明
    "placeMonth": "",  # 报单月份
    "placeMonthStr": "",  # 报单月分
    "productCode": "",  # 商品编码
    "startTimeEnd": "",  # 预警开始时间截止
    "startTimeStart": "",  # 预警开始时间起始
    "state": "",  # 状态（0：停止，1：启用；2：待审核；3审核不通过）
    "warningDimension": "",  # 预警维度（0：代表全部，1：自购预警，2：交付预警）
    "warningName": "",  # 预警名称
    "warningProduct": "",  # 预警产品(0:所有产品；1：单一产品)
    "warningType": "",  # 预警类型（0：数量；1：PV; 2: 金额）
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_dataAdmin_warningRule_list(params=params, headers=headers):
    """
    数据中心管理后台-预警规则管理-获取预警规则列表
    /mgmt/dataAdmin/warningRule/list

    参数说明:
    - controlMemberAuthority: 管控会员权限(0:不管控；1:管控所有；2:管控重点名单)
    - controlStoreAuthority: 管控门店权限(0:不管控；1:管控所有；2:管控重点名单)
    - deliverType: 交付方式;目前只有all
    - endTimeEnd: 预警结束时间截止
    - endTimeStart: 预警结束时间起始
    - isDeliverWarning: //是否交付预警 0:否 1：是
    - isShopWarning: 是否购货预警 0:否 1：是
    - orderWay: 下单方式(0:所有下单方式；1:自购订单 2:代购订单)
    - placeMonth: 报单月份
    - placeMonthStr: 报单月分
    - productCode: 商品编码
    - startTimeEnd: 预警开始时间截止
    - startTimeStart: 预警开始时间起始
    - state: 状态（0：停止，1：启用；2：待审核；3审核不通过）
    - warningDimension: 预警维度（0：代表全部，1：自购预警，2：交付预警）
    - warningName: 预警名称
    - warningProduct: 预警产品(0:所有产品；1：单一产品)
    - warningType: 预警类型（0：数量；1：PV; 2: 金额）
    """

    url = "/mgmt/dataAdmin/warningRule/list"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

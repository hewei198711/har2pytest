import os

from util.client import client

params = {
    "activationResult": 0,  # 开通结果
    "customerIdentity": 0,  # 顾客身份 3->云商 4->微店
    "nameOfPersonInCharge": "",  # 负责人姓名
    "openingTimeEnd": "",  # 开通结束时间
    "openingTimeStart": "",  # 开通开始时间
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 页大小
    "personInChargeCardNumber": "",  # 负责人卡号
    "serviceCenterName": "",  # 服务中心名称
    "serviceCenterNumber": "",  # 服务中心编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_exportPermission(params=params, headers=headers):
    """
    查询开通权限配置记录导出
    /mgmt/store/exportPermission

    参数说明:
    - activationResult: 开通结果
    - customerIdentity: 顾客身份 3->云商 4->微店
    - nameOfPersonInCharge: 负责人姓名
    - openingTimeEnd: 开通结束时间
    - openingTimeStart: 开通开始时间
    - pageNum: 页数
    - pageSize: 页大小
    - personInChargeCardNumber: 负责人卡号
    - serviceCenterName: 服务中心名称
    - serviceCenterNumber: 服务中心编号
    """

    url = "/mgmt/store/exportPermission"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

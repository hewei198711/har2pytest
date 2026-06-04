import os

from util.client import client

data = {
    "activationResult": 0,  # 开通结果
    "customerIdentity": 0,  # 顾客身份 3->云商 4->微店
    "nameOfPersonInCharge": "",  # 负责人姓名
    "openingTimeEnd": "",  # 开通结束时间
    "openingTimeStart": "",  # 开通开始时间
    "pageNum": 0,  # TODO: 添加参数说明
    "pageSize": 0,  # TODO: 添加参数说明
    "personInChargeCardNumber": "",  # 负责人卡号
    "serviceCenterName": "",  # 服务中心名称
    "serviceCenterNumber": "",  # 服务中心编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_findPermissionActivationRecordPage(data=data, headers=headers):
    """
    查询开通权限配置记录
    /mgmt/store/findPermissionActivationRecordPage

    参数说明:
    - activationResult: 开通结果
    - customerIdentity: 顾客身份 3->云商 4->微店
    - nameOfPersonInCharge: 负责人姓名
    - openingTimeEnd: 开通结束时间
    - openingTimeStart: 开通开始时间
    - personInChargeCardNumber: 负责人卡号
    - serviceCenterName: 服务中心名称
    - serviceCenterNumber: 服务中心编号
    """

    url = "/mgmt/store/findPermissionActivationRecordPage"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

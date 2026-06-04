import os

from util.client import client

data = {
    "contractType": 0,  # 合同类型，1/经营合同，2/协议
    "customerId": "",  # 法大大客户编号
    "employeeNumber": "",  # OA工号
    "expireMonth": 0,  # 签署失效期（单位：月份， -1为无限期）
    "id": 0,  # 主键id，如果是修改操作，必传
    "isOnline": 0,  # 是否是线上模板，1/线上，2、线下
    "partyAType": "",  # 签署单位，01000/完美（中国）有限公司，Y0000/扬州完美有限公司
    "scope": "",  # 适用范围，1/服务中心，2/服务公司，多个用英文逗号分隔
    "signType": 0,  # 签署类型：1/单方签署，2/双方签署，3/三方签署
    "templateName": "",  # 合同模板名称
    "templateNo": "",  # 合同模板编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_addOrUpdateContractTemplate(data=data, headers=headers):
    """
    添加合同模板/修改合同模板
    /mgmt/store/addOrUpdateContractTemplate

    参数说明:
    - contractType: 合同类型，1/经营合同，2/协议
    - customerId: 法大大客户编号
    - employeeNumber: OA工号
    - expireMonth: 签署失效期（单位：月份， -1为无限期）
    - id: 主键id，如果是修改操作，必传
    - isOnline: 是否是线上模板，1/线上，2、线下
    - partyAType: 签署单位，01000/完美（中国）有限公司，Y0000/扬州完美有限公司
    - scope: 适用范围，1/服务中心，2/服务公司，多个用英文逗号分隔
    - signType: 签署类型：1/单方签署，2/双方签署，3/三方签署
    - templateName: 合同模板名称
    - templateNo: 合同模板编号
    """

    url = "/mgmt/store/addOrUpdateContractTemplate"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

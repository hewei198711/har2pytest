import os

from util.client import client

params = {
    "contractType": 0,  # 合同类型，1/经营合同，2/协议
    "customerType": 0,  # 客户类型，1/服务中心(默认)，2/服务公司
    "endAddTime": "",  # 添加日期结束时间(yyyy-MM-dd)
    "isOnline": 0,  # 是否是线上模板，1/线上，2、线下
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 每页显示数
    "scope": "",  # 适用范围，1/服务中心，2/服务公司，多个用英文逗号分隔
    "signType": 0,  # 签署类型：1/单方签署，2/双方签署，3/三方签署
    "startAddTime": "",  # 添加日期开始时间(yyyy-MM-dd)
    "templateName": "",  # 模板名称
    "templateStatus": 0,  # 模板状态，1：停用；2：启用
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_queryContractTemplateListPage(params=params, headers=headers):
    """
    分页查询合同模板列表
    /mgmt/store/queryContractTemplateListPage

    参数说明:
    - contractType: 合同类型，1/经营合同，2/协议
    - customerType: 客户类型，1/服务中心(默认)，2/服务公司
    - endAddTime: 添加日期结束时间(yyyy-MM-dd)
    - isOnline: 是否是线上模板，1/线上，2、线下
    - pageNum: 页数
    - pageSize: 每页显示数
    - scope: 适用范围，1/服务中心，2/服务公司，多个用英文逗号分隔
    - signType: 签署类型：1/单方签署，2/双方签署，3/三方签署
    - startAddTime: 添加日期开始时间(yyyy-MM-dd)
    - templateName: 模板名称
    - templateStatus: 模板状态，1：停用；2：启用
    """

    url = "/mgmt/store/queryContractTemplateListPage"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

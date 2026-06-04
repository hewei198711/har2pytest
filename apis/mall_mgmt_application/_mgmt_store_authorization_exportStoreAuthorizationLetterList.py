import os

from util.client import client

params = {
    "companyCode": "",  # 分公司编号
    "endGenerateDate": "",  # 结束生成日期
    "expireDate": "",  # 结束有效期
    "isStoreShow": 0,  # 是否显示于门店系统，0：否，1：是
    "startDate": "",  # 起始有效期
    "startGenerateDate": "",  # 起始生成日期
    "status": 0,  # 授权书状态，0：已失效，1：生效中，2：生成失败
    "storeCode": "",  # 服务中心编号（店铺端必传）
    "templateName": "",  # 授权书模板名称
    "templateNo": "",  # 授权书模板编号
    "year": "",  # 授权书年份
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_authorization_exportStoreAuthorizationLetterList(params=params, headers=headers):
    """
    导出授权书列表
    /mgmt/store/authorization/exportStoreAuthorizationLetterList

    参数说明:
    - companyCode: 分公司编号
    - endGenerateDate: 结束生成日期
    - expireDate: 结束有效期
    - isStoreShow: 是否显示于门店系统，0：否，1：是
    - startDate: 起始有效期
    - startGenerateDate: 起始生成日期
    - status: 授权书状态，0：已失效，1：生效中，2：生成失败
    - storeCode: 服务中心编号（店铺端必传）
    - templateName: 授权书模板名称
    - templateNo: 授权书模板编号
    - year: 授权书年份
    """

    url = "/mgmt/store/authorization/exportStoreAuthorizationLetterList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

import os

from util.client import client

params = {
    "adminMobile": "",  # 企业管理员手机号
    "adminName": "",  # 企业管理员名称
    "certEndTime": "",  # 通过认证开始时间
    "certStartTime": "",  # 通过认证开始时间
    "companyName": "",  # 企业认证名称
    "creditNo": "",  # 认证中统一社会信用代码
    "customerType": 0,  # 客户类型，1/服务中心，2/服务公司，3/个人
    "fddCreditNo": "",  # 法大大统一社会信用代码
    "isReCert": 0,  # 是否需要重新认证，1/是，2/否
    "memberCardNo": "",  # 会员卡号
    "memberId": 0,  # 会员ID
    "pageNum": 0,  # 页码
    "pageSize": 0,  # 每页页数
    "storeCode": "",  # 服务中心编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_getCompanyCertList(params=params, headers=headers):
    """
    获取电子印章认证列表
    /mgmt/store/getCompanyCertList

    参数说明:
    - adminMobile: 企业管理员手机号
    - adminName: 企业管理员名称
    - certEndTime: 通过认证开始时间
    - certStartTime: 通过认证开始时间
    - companyName: 企业认证名称
    - creditNo: 认证中统一社会信用代码
    - customerType: 客户类型，1/服务中心，2/服务公司，3/个人
    - fddCreditNo: 法大大统一社会信用代码
    - isReCert: 是否需要重新认证，1/是，2/否
    - memberCardNo: 会员卡号
    - memberId: 会员ID
    - pageNum: 页码
    - pageSize: 每页页数
    - storeCode: 服务中心编号
    """

    url = "/mgmt/store/getCompanyCertList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

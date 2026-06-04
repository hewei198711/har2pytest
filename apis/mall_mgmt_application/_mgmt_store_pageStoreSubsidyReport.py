import os

from util.client import client

data = {
    "code": "",  # 服务中心编号
    "companyCode": "",  # 所属分公司编号
    "endMonth": "",  # 结束月份，yyyy-MM
    "grade": 0,  # 是否职级，0-否，1-是
    "holdActivity": 0,  # 是否有举办社群活动，0-否，1-是
    "illegal": 0,  # 是否无重大违规，0-否，1-是
    "leaderCardNo": "",  # 负责人卡号
    "pageNum": 0,  # TODO: 添加参数说明
    "pageSize": 0,  # TODO: 添加参数说明
    "send": 0,  # 是否允许发放，0-否，1-是
    "shopType": [],  # 状态名
    "startMonth": "",  # 开始月份，yyyy-MM
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_pageStoreSubsidyReport(data=data, headers=headers):
    """
    分页查询服务中心2%补贴达标报表
    /mgmt/store/pageStoreSubsidyReport

    参数说明:
    - code: 服务中心编号
    - companyCode: 所属分公司编号
    - endMonth: 结束月份，yyyy-MM
    - grade: 是否职级，0-否，1-是
    - holdActivity: 是否有举办社群活动，0-否，1-是
    - illegal: 是否无重大违规，0-否，1-是
    - leaderCardNo: 负责人卡号
    - send: 是否允许发放，0-否，1-是
    - shopType: 状态名
    - startMonth: 开始月份，yyyy-MM
    """

    url = "/mgmt/store/pageStoreSubsidyReport"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

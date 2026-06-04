import os

from util.client import client

params = {
    "accCleanerStatus": 0,  # 状态 -1：已驳回 0：待审核（默认）1：审核通过
    "applicantEndTime": "",  # 申请时间(结束)(格式:yyyy-MM-dd)
    "applicantStartTime": "",  # 申请时间(开始)(格式:yyyy-MM-dd)
    "cardNo": "",  # 服务人员卡号
    "checkEndTime": "",  # 审核时间(结束)(格式:yyyy-MM-dd)
    "checkStartTime": "",  # 审核时间(开始)(格式:yyyy-MM-dd)
    "cleanerMobile": "",  # 服务人员手机
    "cleanerName": "",  # 清洗人名称
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 页大小
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_acc_cleaner_page(params=params, headers=headers):
    """
    分页查询清洗人员
    /mgmt/acc/cleaner/page

    参数说明:
    - accCleanerStatus: 状态 -1：已驳回 0：待审核（默认）1：审核通过
    - applicantEndTime: 申请时间(结束)(格式:yyyy-MM-dd)
    - applicantStartTime: 申请时间(开始)(格式:yyyy-MM-dd)
    - cardNo: 服务人员卡号
    - checkEndTime: 审核时间(结束)(格式:yyyy-MM-dd)
    - checkStartTime: 审核时间(开始)(格式:yyyy-MM-dd)
    - cleanerMobile: 服务人员手机
    - cleanerName: 清洗人名称
    - pageNum: 页数
    - pageSize: 页大小
    """

    url = "/mgmt/acc/cleaner/page"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

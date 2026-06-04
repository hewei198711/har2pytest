import os

from util.client import client

data = {
    "batchNo": "",  # 批次编号
    "cardNo": "",  # 会员卡号
    "isManualAuditList": 0,  # 是否人工审核记录表: 1.是 0.否
    "manualAuditStatus": 0,  # 人工审核状态: -1.未审核 0.审核不通过 1.审核通过 2.已过期
    "manualAuditTimeEnd": "",  # 人工审核时间结束
    "manualAuditTimeStart": "",  # 人工审核时间开始
    "mobile": "",  # 注册手机号
    "pageNum": 0,  # 页码
    "pageSize": 0,  # 每页页数
    "searchMemberType": 0,  # 会员身份 2->VIP会员 3->云商 4->微店
    "thirdPartyAuditStatus": 0,  # 第三方审核状态:-1.待审核 1.审核通过 0.审核不通过
    "userName": "",  # 姓名
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_cms_avatarAudit_getAvatarAuditList(data=data, headers=headers):
    """
    获取用户头像审核记录列表
    /mgmt/cms/avatarAudit/getAvatarAuditList

    参数说明:
    - batchNo: 批次编号
    - cardNo: 会员卡号
    - isManualAuditList: 是否人工审核记录表: 1.是 0.否
    - manualAuditStatus: 人工审核状态: -1.未审核 0.审核不通过 1.审核通过 2.已过期
    - manualAuditTimeEnd: 人工审核时间结束
    - manualAuditTimeStart: 人工审核时间开始
    - mobile: 注册手机号
    - pageNum: 页码
    - pageSize: 每页页数
    - searchMemberType: 会员身份 2->VIP会员 3->云商 4->微店
    - thirdPartyAuditStatus: 第三方审核状态:-1.待审核 1.审核通过 0.审核不通过
    - userName: 姓名
    """

    url = "/mgmt/cms/avatarAudit/getAvatarAuditList"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

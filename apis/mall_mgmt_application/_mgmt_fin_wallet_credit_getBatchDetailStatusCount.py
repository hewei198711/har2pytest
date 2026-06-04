import os

from util.client import client

data = {
    "auditStatus": 0,  # 审批状态：7，待提交，1，待审核，2，审核通过，9，审核不通过。不传查全部
    "batchdtlStatus": 0,  # 生效状态：0：正常；2：已扣减，3：已增加,不传查全部
    "cardNo": "",  # 会员卡号
    "companyCode": "",  # 分公司编号
    "creditDiffAmount": 0,  # 信用额差值，0：等于0,1：其他，不传查全部
    "from": 0,  # TODO: 添加参数说明
    "id": 0,  # 批次ID
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 每页显示数
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_fin_wallet_credit_getBatchDetailStatusCount(data=data, headers=headers):
    """
    云商信用额录入批次详情列表状态统计数据
    /mgmt/fin/wallet/credit/getBatchDetailStatusCount

    参数说明:
    - auditStatus: 审批状态：7，待提交，1，待审核，2，审核通过，9，审核不通过。不传查全部
    - batchdtlStatus: 生效状态：0：正常；2：已扣减，3：已增加,不传查全部
    - cardNo: 会员卡号
    - companyCode: 分公司编号
    - creditDiffAmount: 信用额差值，0：等于0,1：其他，不传查全部
    - id: 批次ID
    - pageNum: 页数
    - pageSize: 每页显示数
    """

    url = "/mgmt/fin/wallet/credit/getBatchDetailStatusCount"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

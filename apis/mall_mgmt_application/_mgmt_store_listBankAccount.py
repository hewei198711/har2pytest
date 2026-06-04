import os

from util.client import client

params = {
    "companyCode": "",  # 分公司编号
    "isSigned": 0,  # 是否已签约，1/是，2/否
    "isUsed": 0,  # 作废标示 1生效 2作废
    "leaderCardNo": "",  # 总店负责人卡号
    "opType": 0,  # 操作类型 1新增 2修改 3作废
    "pageNum": 0,  # pageNum
    "pageSize": 0,  # pageSize
    "storeCode": "",  # 服务中心编号
    "verifyStatus": 0,  # 审核状态 3待审核, 不选则是全部
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_listBankAccount(params=params, headers=headers):
    """
    银行账号列表
    /mgmt/store/listBankAccount

    参数说明:
    - companyCode: 分公司编号
    - isSigned: 是否已签约，1/是，2/否
    - isUsed: 作废标示 1生效 2作废
    - leaderCardNo: 总店负责人卡号
    - opType: 操作类型 1新增 2修改 3作废
    - pageNum: pageNum
    - pageSize: pageSize
    - storeCode: 服务中心编号
    - verifyStatus: 审核状态 3待审核, 不选则是全部
    """

    url = "/mgmt/store/listBankAccount"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

import os

from util.client import client

data = {
    "bankAccount": "",  # 状态
    "bankType": "",  # 签约银行  ICBC：工商银行 PSBC：邮政储蓄银行
    "cardNo": "",  # 会员卡号
    "companyCode": "",  # 分公司编码
    "createTime": "",  # 提交签约时间 时间格式为 yyyy-MM-dd
    "from": 0,  # TODO: 添加参数说明
    "memberType": "",  # 顾客类型
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 每页显示数
    "status": "",  # 状态
    "storeCode": "",  # 服务中心编号
    "tel": "",  # 手机号码
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_fin_wallet_bank_querySignFinWalletBank(data=data, headers=headers):
    """
    签约银行卡信息查询(商城后台)
    /mgmt/fin/wallet/bank/querySignFinWalletBank

    参数说明:
    - bankAccount: 状态
    - bankType: 签约银行  ICBC：工商银行 PSBC：邮政储蓄银行
    - cardNo: 会员卡号
    - companyCode: 分公司编码
    - createTime: 提交签约时间 时间格式为 yyyy-MM-dd
    - memberType: 顾客类型
    - pageNum: 页数
    - pageSize: 每页显示数
    - status: 状态
    - storeCode: 服务中心编号
    - tel: 手机号码
    """

    url = "/mgmt/fin/wallet/bank/querySignFinWalletBank"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

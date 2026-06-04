import os

from util.client import client

data = {
    "beginOverdueDays": 0,  # 逾期天数开区间
    "beginOverdueDaysCount1": 0,  # 逾期8-15天数开区间
    "beginOverdueDaysCount2": 0,  # 逾期16天数开区间
    "cardNo": "",  # 会员卡号
    "cardType": 0,  # 顾客类型，1：普通顾客；2：优惠顾客；3：云商；4：微店
    "companyCode": "",  # 分公司编号
    "creditEnable": False,  # 是否有信用额
    "creditStagesEnable": False,  # 是否有分期
    "endOverdueDays": 0,  # 逾期天数闭区间
    "endOverdueDaysCount1": 0,  # 逾期8-15天数闭区间
    "endOverdueDaysCount2": 0,  # 逾期16天数闭区间
    "from": 0,  # TODO: 添加参数说明
    "negativeEnable": False,  # 钱包可用余额是否为负
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 每页显示数
    "realName": "",  # 会员姓名
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_fin_wallet_credit_stages_queryCreditRepaymentReport(data=data, headers=headers):
    """
    信用额还款情况报表
    /mgmt/fin/wallet/credit/stages/queryCreditRepaymentReport

    参数说明:
    - beginOverdueDays: 逾期天数开区间
    - beginOverdueDaysCount1: 逾期8-15天数开区间
    - beginOverdueDaysCount2: 逾期16天数开区间
    - cardNo: 会员卡号
    - cardType: 顾客类型，1：普通顾客；2：优惠顾客；3：云商；4：微店
    - companyCode: 分公司编号
    - creditEnable: 是否有信用额
    - creditStagesEnable: 是否有分期
    - endOverdueDays: 逾期天数闭区间
    - endOverdueDaysCount1: 逾期8-15天数闭区间
    - endOverdueDaysCount2: 逾期16天数闭区间
    - negativeEnable: 钱包可用余额是否为负
    - pageNum: 页数
    - pageSize: 每页显示数
    - realName: 会员姓名
    """

    url = "/mgmt/fin/wallet/credit/stages/queryCreditRepaymentReport"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

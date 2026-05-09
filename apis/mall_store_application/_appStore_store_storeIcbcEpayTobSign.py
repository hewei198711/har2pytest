import os

from util.client import client

data = {
    "accountName": "",  # 账户名
    "accountNo": "",  # 账号
    "businessFlag": "",  # 业务判断:0-签约,1-解约
    "companyNo": "",  # 分公司编号
    "dayLimitAmt": 0,  # 日累计限额（元）
    "memberId": "",  # 会员id
    "mobile": "",  # 手机号
    "prtlEndDate": "",  # 协议终止日期,格式yyyy-MM-dd
    "trxLimitAmt": 0,  # 单笔限额（元）
    "userCode": "",  # 用户号,在工行端唯一
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_storeIcbcEpayTobSign(data=data, headers=headers):
    """
    获取工行签约/解约链接
    /appStore/store/storeIcbcEpayTobSign

    参数说明:
    - accountName: 账户名
    - accountNo: 账号
    - businessFlag: 业务判断:0-签约,1-解约
    - companyNo: 分公司编号
    - dayLimitAmt: 日累计限额（元）
    - memberId: 会员id
    - mobile: 手机号
    - prtlEndDate: 协议终止日期,格式yyyy-MM-dd
    - trxLimitAmt: 单笔限额（元）
    - userCode: 用户号,在工行端唯一
    """

    url = "/appStore/store/storeIcbcEpayTobSign"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

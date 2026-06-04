import os

from util.client import client

data = {
    "autoType": 0,  # 自动/手工，参数说明 1：自动；2：手工；
    "cardNo": "",  # 会员卡号
    "companyCode": "",  # 分公司编号不能为空
    "endTime": "",  # 到账结束时间
    "from": 0,  # TODO: 添加参数说明
    "memberNo": "",  # 顾客编号
    "memberTypeList": [],  # 顾客类型 1：普通顾客；2：优惠顾客；3：云商；4：微店
    "mobile": "",  # 普客手机号
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 每页显示数
    "startTime": "",  # 到账开始时间
    "transMethod": 0,  # 交易方式：101：平安  203：邮政储蓄银行、201：工商银行、103：交通银行、202：建行银行、206：工商分期付、 106：数字人民币
    "transTime": "",  # 查询月份，格式：yyyy-MM,例如：8月：2020-08
    "transType": 0,  # 账款类型, 参数说明：1：充值；2：购货转入；6：提现；7：原路退款；9:还欠款；10；补银行流水；11：手工退款；12：押货款与钱包互转；13：其他；16：定金转入；21：签约款汇入
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_fin_wallet_bill_queryFinWalletCompanyAccountTrans(data=data, headers=headers):
    """
    查询分公司银行流水(商城后台)
    /mgmt/fin/wallet/bill/queryFinWalletCompanyAccountTrans

    参数说明:
    - autoType: 自动/手工，参数说明 1：自动；2：手工；
    - cardNo: 会员卡号
    - companyCode: 分公司编号不能为空
    - endTime: 到账结束时间
    - memberNo: 顾客编号
    - memberTypeList: 顾客类型 1：普通顾客；2：优惠顾客；3：云商；4：微店
    - mobile: 普客手机号
    - pageNum: 页数
    - pageSize: 每页显示数
    - startTime: 到账开始时间
    - transMethod: 交易方式：101：平安  203：邮政储蓄银行、201：工商银行、103：交通银行、202：建行银行、206：工商分期付、 106：数字人民币
    - transTime: 查询月份，格式：yyyy-MM,例如：8月：2020-08
    - transType: 账款类型, 参数说明：1：充值；2：购货转入；6：提现；7：原路退款；9:还欠款；10；补银行流水；11：手工退款；12：押货款与钱包互转；13：其他；16：定金转入；21：签约款汇入
    """

    url = "/mgmt/fin/wallet/bill/queryFinWalletCompanyAccountTrans"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

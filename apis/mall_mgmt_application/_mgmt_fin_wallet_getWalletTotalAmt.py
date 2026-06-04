import os

from util.client import client

data = {
    "cardNo": "",  # 会员卡号
    "cardType": 0,  # 顾客类型，1：普通顾客；2：优惠顾客；3：云商；4：微店
    "cardTypeList": [],  # 顾客类型，1：普通顾客；2：优惠顾客；3：云商；4：微店
    "companyCode": "",  # 分公司编号
    "creditEnable": False,  # 是否有信用额
    "from": 0,  # TODO: 添加参数说明
    "memberId": 0,  # 顾客编号
    "mobile": "",  # 顾客手机号
    "negativeEnable": False,  # 钱包余额为负
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 每页显示数
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_fin_wallet_getWalletTotalAmt(data=data, headers=headers):
    """
    获取钱包合计金额
    /mgmt/fin/wallet/getWalletTotalAmt

    参数说明:
    - cardNo: 会员卡号
    - cardType: 顾客类型，1：普通顾客；2：优惠顾客；3：云商；4：微店
    - cardTypeList: 顾客类型，1：普通顾客；2：优惠顾客；3：云商；4：微店
    - companyCode: 分公司编号
    - creditEnable: 是否有信用额
    - memberId: 顾客编号
    - mobile: 顾客手机号
    - negativeEnable: 钱包余额为负
    - pageNum: 页数
    - pageSize: 每页显示数
    """

    url = "/mgmt/fin/wallet/getWalletTotalAmt"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

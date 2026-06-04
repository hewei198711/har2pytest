import os

from util.client import client

data = {
    "cardNo": "",  # 会员卡号
    "commitSignDate": "",  # 提交签约日期 yyyy-MM-dd
    "companyCode": "",  # 公司编码
    "from": 0,  # TODO: 添加参数说明
    "memberType": "",  # 会员类型 1：普客 2：优惠顾客 3：云商 4：微店
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 每页显示数
    "registerTel": "",  # 手机号
    "signEntrance": "",  # 签约入口 1、常规 2、签约购
    "signStatus": "",  # 状态 0-绑定；1-解绑
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_fin_wallet_queryFinSignPayBankCard(data=data, headers=headers):
    """
    查询分期付工行绑卡信息
    /mgmt/fin/wallet/queryFinSignPayBankCard

    参数说明:
    - cardNo: 会员卡号
    - commitSignDate: 提交签约日期 yyyy-MM-dd
    - companyCode: 公司编码
    - memberType: 会员类型 1：普客 2：优惠顾客 3：云商 4：微店
    - pageNum: 页数
    - pageSize: 每页显示数
    - registerTel: 手机号
    - signEntrance: 签约入口 1、常规 2、签约购
    - signStatus: 状态 0-绑定；1-解绑
    """

    url = "/mgmt/fin/wallet/queryFinSignPayBankCard"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

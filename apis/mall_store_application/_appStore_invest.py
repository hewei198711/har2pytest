import os

from util.client import client

data = {
    "accountName": "",  # 户名不能为空
    "bankAccount": "",  # 代扣账户不能为空
    "bankName": "",  # 开户银行名称
    "businessType": 0,  # 业务类型 1-> 库存转移支付  2->押货下单支付  3-> 充值
    "identificNo": "",  # 缴费编号
    "payAmount": 0.0,  # 充值金额
    "payChannel": "",  # 充值渠道 WEB/APP
    "payType": 0,  # 2->工行签约代扣   3->建行签约代扣
    "storeCode": "",  # 店铺编号
    "userId": "",  # 用户ID
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_invest(data=data, headers=headers):
    """
    充值
    /appStore/invest

    参数说明:
    - accountName: 户名不能为空
    - bankAccount: 代扣账户不能为空
    - bankName: 开户银行名称
    - businessType: 业务类型 1-> 库存转移支付  2->押货下单支付  3-> 充值
    - identificNo: 缴费编号
    - payAmount: 充值金额
    - payChannel: 充值渠道 WEB/APP
    - payType: 2->工行签约代扣   3->建行签约代扣
    - storeCode: 店铺编号
    - userId: 用户ID
    """

    url = "/appStore/invest"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

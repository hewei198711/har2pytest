import os

from util.client import client

data = {
    "accountName": "",  # 户名
    "bankAccount": "",  # 代扣账户
    "bankName": "",  # 开户银行名称
    "businessType": 0,  # 业务类型 1-> 库存转移支付  2->押货下单支付  3-> 充值 4-> 签约购支付
    "depositAmount": 0.0,  # 支付时保证金余额
    "extJson": "",  # 扩展参数
    "identificNo": "",  # 代扣缴费编号
    "mortgageType": 0,  # 押货下单细分类型  1->普通押货下单  2->随心购押货下单, 3->签约购押货下单(2.0),4->签约购押货下单(3.0),5->签约购押货下单(4.0)
    "payAmount": 0.0,  # 支付金额
    "payChannel": "",  # 支付渠道 WEB/APP/PC/applet
    "payType": 0,  # 支付方式 1-> 保证金  2->工行签约代扣   3->建行签约代扣  4->工行代扣、保证金组合支付, 5->建行代扣、保证金组合支付
    "protocolOrderNo": "",  # 签约单子单号
    "pxAmount": 0.0,  # 拼箱费
    "storeCode": "",  # 店铺编号
    "sxgOrderNo": "",  # 随心购单号
    "uniqueFlagNo": "",  # 订单唯一标识
    "userId": "",  # 用户ID
    "yfAmount": 0.0,  # 运费
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _appStore_api_wallet_pay(data=data, headers=headers):
    """
    支付
    /appStore/api/wallet/pay

    参数说明:
    - accountName: 户名
    - bankAccount: 代扣账户
    - bankName: 开户银行名称
    - businessType: 业务类型 1-> 库存转移支付  2->押货下单支付  3-> 充值 4-> 签约购支付
    - depositAmount: 支付时保证金余额
    - extJson: 扩展参数
    - identificNo: 代扣缴费编号
    - mortgageType: 押货下单细分类型  1->普通押货下单  2->随心购押货下单, 3->签约购押货下单(2.0),4->签约购押货下单(3.0),5->签约购押货下单(4.0)
    - payAmount: 支付金额
    - payChannel: 支付渠道 WEB/APP/PC/applet
    - payType: 支付方式 1-> 保证金  2->工行签约代扣   3->建行签约代扣  4->工行代扣、保证金组合支付, 5->建行代扣、保证金组合支付
    - protocolOrderNo: 签约单子单号
    - pxAmount: 拼箱费
    - storeCode: 店铺编号
    - sxgOrderNo: 随心购单号
    - uniqueFlagNo: 订单唯一标识
    - userId: 用户ID
    - yfAmount: 运费
    """

    url = "/appStore/api/wallet/pay"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

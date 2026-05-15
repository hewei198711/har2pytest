import os

from util.client import client

data = {
    "isFirst": False,  # 是否首单  true： 是    false： 否
    "mortgageOrderNo": "",  # 押货单号
    "payDTO": {
        "accountName": "",
        "bankAccount": "",
        "bankName": "",
        "businessType": 0,
        "depositAmount": 0.0,
        "extJson": "",
        "identificNo": "",
        "mortgageType": 0,
        "payAmount": 0.0,
        "payChannel": "",
        "payType": 0,
        "protocolOrderNo": "",
        "pxAmount": 0.0,
        "storeCode": "",
        "sxgOrderNo": "",
        "uniqueFlagNo": "",
        "userId": "",
        "yfAmount": 0.0,
    },  # 支付主体参数
    "protocolOrderNo": "",  # 签约单号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _appStore_api_wallet_protocolPay(data=data, headers=headers):
    """
    签约购支付
    /appStore/api/wallet/protocolPay

    参数说明:
    - isFirst: 是否首单  true： 是    false： 否
    - mortgageOrderNo: 押货单号
    - payDTO: 支付主体参数
    - payDTO.accountName: 户名
    - payDTO.bankAccount: 代扣账户
    - payDTO.bankName: 开户银行名称
    - payDTO.businessType: 业务类型 1-> 库存转移支付  2->押货下单支付  3-> 充值 4-> 签约购支付
    - payDTO.depositAmount: 支付时保证金余额
    - payDTO.extJson: 扩展参数
    - payDTO.identificNo: 代扣缴费编号
    - payDTO.mortgageType: 押货下单细分类型  1->普通押货下单  2->随心购押货下单, 3->签约购押货下单(2.0),4->签约购押货下单(3.0),5->签约购押货下单(4.0)
    - payDTO.payAmount: 支付金额
    - payDTO.payChannel: 支付渠道 WEB/APP/PC/applet
    - payDTO.payType: 支付方式 1-> 保证金  2->工行签约代扣   3->建行签约代扣  4->工行代扣、保证金组合支付, 5->建行代扣、保证金组合支付
    - payDTO.protocolOrderNo: 签约单子单号
    - payDTO.pxAmount: 拼箱费
    - payDTO.storeCode: 店铺编号
    - payDTO.sxgOrderNo: 随心购单号
    - payDTO.uniqueFlagNo: 订单唯一标识
    - payDTO.userId: 用户ID
    - payDTO.yfAmount: 运费
    - protocolOrderNo: 签约单号
    """

    url = "/appStore/api/wallet/protocolPay"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

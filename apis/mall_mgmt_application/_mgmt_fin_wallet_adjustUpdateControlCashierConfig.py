import os

from util.client import client

data = {
    "batchCode": "",  # 风控批次码
    "channelCode": "",  # 支付通道编码 101、微信支付;102、支付宝支付;103、银联;106、数字人民币 201、工商银行;202、建设银行;203、邮政储蓄银行;
    "companyInfoList": [{"companyCode": "", "companyName": ""}],  # 受控/被控分公司编号集合
    "controlSource": 0,  # 管控来源 1、内部 2、外部单位
    "memberTypeList": [],  # 会员类别：1->普通顾客；2->优惠顾客；3->云商；4->微店（云+）
    "paytypeCode": [],  # 商城登录入口类型 APP、PC、PROGRAM
    "remark": "",  # 原因及备注说明
    "restrictedDate": "",  # 受限/被控开始时间 yyyy-MM-dd
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_fin_wallet_adjustUpdateControlCashierConfig(data=data, headers=headers):
    """
    调整管控列表
    /mgmt/fin/wallet/adjustUpdateControlCashierConfig

    参数说明:
    - batchCode: 风控批次码
    - channelCode: 支付通道编码 101、微信支付;102、支付宝支付;103、银联;106、数字人民币 201、工商银行;202、建设银行;203、邮政储蓄银行;
    - companyInfoList: 受控/被控分公司编号集合
    - companyInfoList.companyCode: 公司编号
    - companyInfoList.companyName: 公司名称
    - controlSource: 管控来源 1、内部 2、外部单位
    - memberTypeList: 会员类别：1->普通顾客；2->优惠顾客；3->云商；4->微店（云+）
    - paytypeCode: 商城登录入口类型 APP、PC、PROGRAM
    - remark: 原因及备注说明
    - restrictedDate: 受限/被控开始时间 yyyy-MM-dd
    """

    url = "/mgmt/fin/wallet/adjustUpdateControlCashierConfig"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

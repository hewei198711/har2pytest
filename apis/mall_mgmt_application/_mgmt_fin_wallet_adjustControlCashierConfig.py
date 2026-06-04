import os

from util.client import client

data = {
    "cancelConfigReqDto": {
        "batchCode": "",
        "channelCode": "",
        "companyInfoList": [{"companyCode": "", "companyName": ""}],
        "controlSource": 0,
        "memberTypeList": [],
        "paytypeCode": [],
        "remark": "",
        "restrictedDate": "",
    },  # 批次渠道取消数据 涉及到 公司、顾客类型、商城入口三个维度
    "insertCashierConfigReqDto": {
        "batchCode": "",
        "channelCode": "",
        "companyInfoList": [{"companyCode": "", "companyName": ""}],
        "controlSource": 0,
        "memberTypeList": [],
        "paytypeCode": [],
        "remark": "",
        "restrictedDate": "",
    },  # 批次渠道新增数据 涉及到 公司、顾客类型、商城入口三个维度
    "updateConfigReqDto": {
        "batchCode": "",
        "channelCode": "",
        "companyInfoList": [{"companyCode": "", "companyName": ""}],
        "controlSource": 0,
        "memberTypeList": [],
        "paytypeCode": [],
        "remark": "",
        "restrictedDate": "",
    },  # 批次渠道更新数据 涉及到 公司、顾客类型、商城入口三个维度
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_fin_wallet_adjustControlCashierConfig(data=data, headers=headers):
    """
    调整管控列表
    /mgmt/fin/wallet/adjustControlCashierConfig

    参数说明:
    - cancelConfigReqDto: 批次渠道取消数据 涉及到 公司、顾客类型、商城入口三个维度
    - cancelConfigReqDto.batchCode: 风控批次码
    - cancelConfigReqDto.channelCode: 支付通道编码 101、微信支付;102、支付宝支付;103、银联;106、数字人民币 201、工商银行;202、建设银行;203、邮政储蓄银行;
    - cancelConfigReqDto.companyInfoList: 受控/被控分公司编号集合
    - cancelConfigReqDto.companyInfoList.companyCode: 公司编号
    - cancelConfigReqDto.companyInfoList.companyName: 公司名称
    - cancelConfigReqDto.controlSource: 管控来源 1、内部 2、外部单位
    - cancelConfigReqDto.memberTypeList: 会员类别：1->普通顾客；2->优惠顾客；3->云商；4->微店（云+）
    - cancelConfigReqDto.paytypeCode: 商城登录入口类型 APP、PC、PROGRAM
    - cancelConfigReqDto.remark: 原因及备注说明
    - cancelConfigReqDto.restrictedDate: 受限/被控开始时间 yyyy-MM-dd
    - insertCashierConfigReqDto: 批次渠道新增数据 涉及到 公司、顾客类型、商城入口三个维度
    - insertCashierConfigReqDto.batchCode: 风控批次码
    - insertCashierConfigReqDto.channelCode: 支付通道编码 101、微信支付;102、支付宝支付;103、银联;106、数字人民币 201、工商银行;202、建设银行;203、邮政储蓄银行;
    - insertCashierConfigReqDto.companyInfoList: 受控/被控分公司编号集合
    - insertCashierConfigReqDto.companyInfoList.companyCode: 公司编号
    - insertCashierConfigReqDto.companyInfoList.companyName: 公司名称
    - insertCashierConfigReqDto.controlSource: 管控来源 1、内部 2、外部单位
    - insertCashierConfigReqDto.memberTypeList: 会员类别：1->普通顾客；2->优惠顾客；3->云商；4->微店（云+）
    - insertCashierConfigReqDto.paytypeCode: 商城登录入口类型 APP、PC、PROGRAM
    - insertCashierConfigReqDto.remark: 原因及备注说明
    - insertCashierConfigReqDto.restrictedDate: 受限/被控开始时间 yyyy-MM-dd
    - updateConfigReqDto: 批次渠道更新数据 涉及到 公司、顾客类型、商城入口三个维度
    - updateConfigReqDto.batchCode: 风控批次码
    - updateConfigReqDto.channelCode: 支付通道编码 101、微信支付;102、支付宝支付;103、银联;106、数字人民币 201、工商银行;202、建设银行;203、邮政储蓄银行;
    - updateConfigReqDto.companyInfoList: 受控/被控分公司编号集合
    - updateConfigReqDto.companyInfoList.companyCode: 公司编号
    - updateConfigReqDto.companyInfoList.companyName: 公司名称
    - updateConfigReqDto.controlSource: 管控来源 1、内部 2、外部单位
    - updateConfigReqDto.memberTypeList: 会员类别：1->普通顾客；2->优惠顾客；3->云商；4->微店（云+）
    - updateConfigReqDto.paytypeCode: 商城登录入口类型 APP、PC、PROGRAM
    - updateConfigReqDto.remark: 原因及备注说明
    - updateConfigReqDto.restrictedDate: 受限/被控开始时间 yyyy-MM-dd
    """

    url = "/mgmt/fin/wallet/adjustControlCashierConfig"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

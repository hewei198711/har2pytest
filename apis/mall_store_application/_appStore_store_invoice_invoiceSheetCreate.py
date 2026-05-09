import os

from util.client import client

data = {
    "applyCardNo": "",  # 申请人卡号
    "applyCardType": 0,  # 申请人卡类型
    "applyMemberId": 0,  # 申请人id
    "applyMobile": "",  # 申请人手机号码
    "applyRealname": "",  # 申请人姓名
    "cardNo": "",  # 会员卡号
    "cardType": 0,  # 顾客类型，1：普通顾客；2：优惠顾客；3：云商；4：微店
    "chargeType": 0,  # 费用类型，1：服务费；2：交付服务费（跨省云+店铺需要传这个参数）
    "invoiceIds": "",  # 所选发票记录唯一性id组合，用【,】分隔
    "invoiceTotalMoney": 0.0,  # 所选发票合计含税金额，主要用于防呆校验
    "memberId": 0,  # 用户id
    "mobile": "",  # 手机号码
    "paymentCompanyCode": "",  # 出款公司编号
    "paymentCompanyName": "",  # 出款公司名称
    "realname": "",  # 姓名
    "serviceCenterNo": "",  # 服务公司/服务中心编号，主要用于防呆校验
    "serviceName": "",  # 服务公司/服务中心名称
    "serviceType": 0,  # 服务类型，1：服务公司；2：服务中心
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_invoice_invoiceSheetCreate(data=data, headers=headers):
    """
    计算表.生成计算表，返回唯一性Id
    /appStore/store/invoice/invoiceSheetCreate

    参数说明:
    - applyCardNo: 申请人卡号
    - applyCardType: 申请人卡类型
    - applyMemberId: 申请人id
    - applyMobile: 申请人手机号码
    - applyRealname: 申请人姓名
    - cardNo: 会员卡号
    - cardType: 顾客类型，1：普通顾客；2：优惠顾客；3：云商；4：微店
    - chargeType: 费用类型，1：服务费；2：交付服务费（跨省云+店铺需要传这个参数）
    - invoiceIds: 所选发票记录唯一性id组合，用【,】分隔
    - invoiceTotalMoney: 所选发票合计含税金额，主要用于防呆校验
    - memberId: 用户id
    - mobile: 手机号码
    - paymentCompanyCode: 出款公司编号
    - paymentCompanyName: 出款公司名称
    - realname: 姓名
    - serviceCenterNo: 服务公司/服务中心编号，主要用于防呆校验
    - serviceName: 服务公司/服务中心名称
    - serviceType: 服务类型，1：服务公司；2：服务中心
    """

    url = "/appStore/store/invoice/invoiceSheetCreate"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

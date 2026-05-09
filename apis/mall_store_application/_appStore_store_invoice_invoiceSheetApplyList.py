import os

from util.client import client

data = {
    "applyEndTime": "",  # 申请结束时间
    "applyStartTime": "",  # 申请开始时间
    "applyStatus": 0,  # 状态，1：待服务公司/服务中心签署；2：待完美公司签署；3：已完成；4：服务公司/中心已拒签；5：完美公司已拒签；6：已作废
    "applyStatusList": [],  # 状态集合，签署中传1,2；已完成传3；已拒签传4,5
    "cardNo": "",  # 会员卡号
    "cardType": 0,  # 顾客类型，1：普通顾客；2：优惠顾客；3：云商；4：微店
    "from": 0,  # TODO: 添加参数说明
    "memberId": 0,  # 用户id
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 每页显示数
    "paymentCompanyCode": "",  # 出款公司编号
    "paymentCompanyName": "",  # 出款公司名称
    "platformType": 0,  # 平台类型，前端不用传递此参数
    "serviceCode": "",  # 服务公司/服务中心编号
    "serviceName": "",  # 服务公司/服务中心名称
    "serviceType": 0,  # 服务类型，1：服务公司；2：服务中心
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_invoice_invoiceSheetApplyList(data=data, headers=headers):
    """
    计算表.申请记录
    /appStore/store/invoice/invoiceSheetApplyList

    参数说明:
    - applyEndTime: 申请结束时间
    - applyStartTime: 申请开始时间
    - applyStatus: 状态，1：待服务公司/服务中心签署；2：待完美公司签署；3：已完成；4：服务公司/中心已拒签；5：完美公司已拒签；6：已作废
    - applyStatusList: 状态集合，签署中传1,2；已完成传3；已拒签传4,5
    - cardNo: 会员卡号
    - cardType: 顾客类型，1：普通顾客；2：优惠顾客；3：云商；4：微店
    - memberId: 用户id
    - pageNum: 页数
    - pageSize: 每页显示数
    - paymentCompanyCode: 出款公司编号
    - paymentCompanyName: 出款公司名称
    - platformType: 平台类型，前端不用传递此参数
    - serviceCode: 服务公司/服务中心编号
    - serviceName: 服务公司/服务中心名称
    - serviceType: 服务类型，1：服务公司；2：服务中心
    """

    url = "/appStore/store/invoice/invoiceSheetApplyList"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

import os

from util.client import client

params = {
    "companyCode": "",  # 分公司编号
    "companyCodes": [],  # 分公司编号列表
    "companySignPerson": "",  # 公司签署人
    "isSignOffline": 0,  # 是否线下签署
    "maxBillMonth": 0,  # 对账单月份最大值，格式: yyyymm
    "maxSignEndDate": "",  # 店铺签署截止日期最大值，格式yyyy-MM-dd
    "maxSignStartDate": "",  # 发起签署日期最大值，格式yyyy-MM-dd
    "maxStoreSignDate": "",  # 店铺签署时间最大值，格式yyyy-MM-dd
    "minBillMonth": 0,  # 对账单月份最小值，格式: yyyymm
    "minSignEndDate": "",  # 店铺签署截止日期最小值，格式yyyy-MM-dd
    "minSignStartDate": "",  # 发起签署日期最小值，格式yyyy-MM-dd
    "minStoreSignDate": "",  # 店铺签署时间最小值，格式yyyy-MM-dd
    "orderType": 0,  # TODO: 添加参数说明
    "pageNum": 0,  # 页码
    "pageSize": 0,  # 每页页数
    "signStatus": 0,  # 签署状态，1/待提交，2/待店铺签署，3/待公司签署，4/签署完成，5/超时中止签署，6/拒签，7/已撤回，8/已作废，9/生成失败
    "signStatusArr": "",  # 签署状态，多个用逗号分隔
    "signType": 0,  # 对账单签署类型，1/1:3库存对账单，2/85%库存对账单，3/85%账款对账单，4/钱包对账单
    "storeCode": "",  # 服务中心编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_contract_exportStoreContractInvtBillList(params=params, headers=headers):
    """
    导出库存对账单合同列表
    /mgmt/store/contract/exportStoreContractInvtBillList

    参数说明:
    - companyCode: 分公司编号
    - companyCodes: 分公司编号列表
    - companySignPerson: 公司签署人
    - isSignOffline: 是否线下签署
    - maxBillMonth: 对账单月份最大值，格式: yyyymm
    - maxSignEndDate: 店铺签署截止日期最大值，格式yyyy-MM-dd
    - maxSignStartDate: 发起签署日期最大值，格式yyyy-MM-dd
    - maxStoreSignDate: 店铺签署时间最大值，格式yyyy-MM-dd
    - minBillMonth: 对账单月份最小值，格式: yyyymm
    - minSignEndDate: 店铺签署截止日期最小值，格式yyyy-MM-dd
    - minSignStartDate: 发起签署日期最小值，格式yyyy-MM-dd
    - minStoreSignDate: 店铺签署时间最小值，格式yyyy-MM-dd
    - pageNum: 页码
    - pageSize: 每页页数
    - signStatus: 签署状态，1/待提交，2/待店铺签署，3/待公司签署，4/签署完成，5/超时中止签署，6/拒签，7/已撤回，8/已作废，9/生成失败
    - signStatusArr: 签署状态，多个用逗号分隔
    - signType: 对账单签署类型，1/1:3库存对账单，2/85%库存对账单，3/85%账款对账单，4/钱包对账单
    - storeCode: 服务中心编号
    """

    url = "/mgmt/store/contract/exportStoreContractInvtBillList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

import os

from util.client import client

params = {
    "isSignOffline": 0,  # 是否已线下签署，0/否，1/是
    "maxBillMonth": 0,  # 对账单月份最大值，格式: yyyymm
    "maxSignEndDate": "",  # 店铺签署截止日期最大值，格式yyyy-MM-dd
    "maxStoreSignDate": "",  # 店铺签署时间最大值，格式yyyy-MM-dd
    "minBillMonth": 0,  # 对账单月份最小值，格式: yyyymm
    "minSignEndDate": "",  # 店铺签署截止日期最小值，格式yyyy-MM-dd
    "minStoreSignDate": "",  # 店铺签署时间最小值，格式yyyy-MM-dd
    "pageNum": 0,  # 页码
    "pageSize": 0,  # 每页页数
    "signStatus": 0,  # 签署状态，2/待店铺签署，4/签署完成，5/超时中止签署，6/拒签
    "signType": 0,  # 签署类型，1/1:3库存对账单，2/85%库存对账单，3/85%账款对账单，4/钱包对账单
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_contract_getStoreContractInvtBillList(params=params, headers=headers):
    """
    查询库存对账单合同列表
    /appStore/store/contract/getStoreContractInvtBillList

    参数说明:
    - isSignOffline: 是否已线下签署，0/否，1/是
    - maxBillMonth: 对账单月份最大值，格式: yyyymm
    - maxSignEndDate: 店铺签署截止日期最大值，格式yyyy-MM-dd
    - maxStoreSignDate: 店铺签署时间最大值，格式yyyy-MM-dd
    - minBillMonth: 对账单月份最小值，格式: yyyymm
    - minSignEndDate: 店铺签署截止日期最小值，格式yyyy-MM-dd
    - minStoreSignDate: 店铺签署时间最小值，格式yyyy-MM-dd
    - pageNum: 页码
    - pageSize: 每页页数
    - signStatus: 签署状态，2/待店铺签署，4/签署完成，5/超时中止签署，6/拒签
    - signType: 签署类型，1/1:3库存对账单，2/85%库存对账单，3/85%账款对账单，4/钱包对账单
    """

    url = "/appStore/store/contract/getStoreContractInvtBillList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

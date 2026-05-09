import os

from util.client import client

params = {
    "beginTime": "",  # 开始时间
    "companyCode": "",  # 分公司编号
    "companyCodeList": [],  # 分公司编号列表
    "companyCodes": [],  # TODO: 添加参数说明
    "endTime": "",  # 结束时间
    "exchangeType": 0,  # 换货类型 1先退后换 2秒换 3只换不退 4先换后退
    "orderSn": "",  # 换货单编号
    "orderSource": 0,  # 来源 1服务中心换货 2运营后台换货
    "orderStatus": 0,  # 1待审核 2待退回 3待验货 4待发货 5待收货 6已完成 7已取消
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 页大小
    "pushStatus": 0,  # 推送状态 1待推送 2推送成功
    "reasonFirst": "",  # 一级原因
    "reasonSecond": "",  # 二级原因
    "returnType": 0,  # 退回方式 1服务中心报废 2自带 3邮寄 4上门取件
    "storeCode": "",  # 服务中心编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_dis_mortgage_exchangeOrder_listExportExcel(params=params, headers=headers):
    """
    导出换货单列表
    /appStore/store/dis/mortgage/exchangeOrder/listExportExcel

    参数说明:
    - beginTime: 开始时间
    - companyCode: 分公司编号
    - companyCodeList: 分公司编号列表
    - endTime: 结束时间
    - exchangeType: 换货类型 1先退后换 2秒换 3只换不退 4先换后退
    - orderSn: 换货单编号
    - orderSource: 来源 1服务中心换货 2运营后台换货
    - orderStatus: 1待审核 2待退回 3待验货 4待发货 5待收货 6已完成 7已取消
    - pageNum: 页数
    - pageSize: 页大小
    - pushStatus: 推送状态 1待推送 2推送成功
    - reasonFirst: 一级原因
    - reasonSecond: 二级原因
    - returnType: 退回方式 1服务中心报废 2自带 3邮寄 4上门取件
    - storeCode: 服务中心编号
    """

    url = "/appStore/store/dis/mortgage/exchangeOrder/listExportExcel"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

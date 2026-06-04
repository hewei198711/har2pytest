import os

from util.client import client

params = {
    "beginDate": "",  # 开始时间
    "companyCode": "",  # 服务中心所属分公司编码
    "endDate": "",  # 结束时间
    "financeCompanyCode": "",  # 订单财务分公司编码
    "from": 0,  # TODO: 添加参数说明
    "orderNo": "",  # 订单编码
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 每页显示数
    "storeCode": "",  # 服务中心编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_order_exportOrderStoreDiffDetailList(params=params, headers=headers):
    """
    门店自提订单分公司不一致（明细表） - 按订单
    /mgmt/order/exportOrderStoreDiffDetailList

    参数说明:
    - beginDate: 开始时间
    - companyCode: 服务中心所属分公司编码
    - endDate: 结束时间
    - financeCompanyCode: 订单财务分公司编码
    - orderNo: 订单编码
    - pageNum: 页数
    - pageSize: 每页显示数
    - storeCode: 服务中心编号
    """

    url = "/mgmt/order/exportOrderStoreDiffDetailList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

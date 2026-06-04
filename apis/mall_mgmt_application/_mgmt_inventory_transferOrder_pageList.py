import os

from util.client import client

data = {
    "companyCode": "",  # 分公司编号
    "customerCardNo": "",  # 会员卡号
    "customerType": 0,  # 顾客类型 1->普通顾客 2->优惠顾客 3->云商 4->微店
    "month": 0,  # 月份(yyyyMM)
    "openOrderCardNo": "",  # 开单人卡号
    "openOrderManType": 0,  # 开单人类型 3->云商 4->微店
    "orderType": 0,  # 账款类型 1->报单 ，2->退单
    "pageNum": 0,  # 第几页
    "pageSize": 0,  # 每页显示页数
    "storeCode": "",  # 服务中心编号
    "verifyEndDay": "",  # 审核结束时间(yyyy-MM-dd)
    "verifyStartDay": "",  # 审核开始时间(yyyy-MM-dd)
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_transferOrder_pageList(data=data, headers=headers):
    """
    分页列表
    /mgmt/inventory/transferOrder/pageList

    参数说明:
    - companyCode: 分公司编号
    - customerCardNo: 会员卡号
    - customerType: 顾客类型 1->普通顾客 2->优惠顾客 3->云商 4->微店
    - month: 月份(yyyyMM)
    - openOrderCardNo: 开单人卡号
    - openOrderManType: 开单人类型 3->云商 4->微店
    - orderType: 账款类型 1->报单 ，2->退单
    - pageNum: 第几页
    - pageSize: 每页显示页数
    - storeCode: 服务中心编号
    - verifyEndDay: 审核结束时间(yyyy-MM-dd)
    - verifyStartDay: 审核开始时间(yyyy-MM-dd)
    """

    url = "/mgmt/inventory/transferOrder/pageList"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

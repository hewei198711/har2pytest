import os

from util.client import client

data = {
    "month": "",  # 年月(yyyy-MM)
    "orderCreateTime": "",  # 创建时间排序的字段
    "pageNum": 0,  # 当前页,默认第1页
    "pageSize": 0,  # 每页显示数,默认10条
    "recordType": 0,  # 调整原因(1配送返还,2商城退货,3押货使用,4押货退货,5押货调整,6库存调整,7汇押货款,8退押货款,9新增押货信誉额,10押货信誉额还款,11产品调价,12汇订货款,13退订货款,14订货下单,15订货退货)
    "storeCode": "",  # 当前用户的StoreCode
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_mortgageAmount_history_invtHistoryMortgageAmountRecord(data=data, headers=headers):
    """
    押货余额增减明细
    /appStore/mortgageAmount/history/invtHistoryMortgageAmountRecord

    参数说明:
    - month: 年月(yyyy-MM)
    - orderCreateTime: 创建时间排序的字段
    - pageNum: 当前页,默认第1页
    - pageSize: 每页显示数,默认10条
    - recordType: 调整原因(1配送返还,2商城退货,3押货使用,4押货退货,5押货调整,6库存调整,7汇押货款,8退押货款,9新增押货信誉额,10押货信誉额还款,11产品调价,12汇订货款,13退订货款,14订货下单,15订货退货)
    - storeCode: 当前用户的StoreCode
    """

    url = "/appStore/mortgageAmount/history/invtHistoryMortgageAmountRecord"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

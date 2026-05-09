import os

from util.client import client

data = {
    "endDay": "",  # 自定义时间(天为单位) -- 结束日期(yyyy-MM-dd)
    "endMonth": "",  # 自定义时间(月为单位) -- 结束月份(yyyy-MM)
    "isPage": 0,  # TODO: 添加参数说明
    "pageNum": 0,  # 第几页
    "pageSize": 0,  # 页数
    "recordType": [],  # 类型 1汇押货款、2 1:3押货退款申请、3新增信誉额、4超额押货款确认押货款、5无法识别款确认押货款、6扣减信誉额、7手工退押货款、8手工增加押货款、9转销售、10押货款还钱包欠款、11钱包款还押货欠款、12其它 13产品调价 14押货支付 15押货退货 16押货调整 17商城订单转押货额 18商城订单转押货额  19 押货保证金转移
    "remitType": 0,  # 款项类型  1 ->汇押货款 2-> 退押货款  12 -> 其他  19->押货保证金转移
    "startDay": "",  # 自定义时间(天为单位) -- 开始日期(yyyy-MM-dd)
    "startMonth": "",  # 自定义时间(月为单位) -- 开始月份(yyyy-MM)
    "storeCode": "",  # 服务中心编号
    "type": 0,  # 1 本月  2 上月   3 本年
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_inventory_mortgageAmount_remitDetailSearchList(data=data, headers=headers):
    """
    服务中心钱包累计汇退款明细(多条件搜索)
    /appStore/store/inventory/mortgageAmount/remitDetailSearchList

    参数说明:
    - endDay: 自定义时间(天为单位) -- 结束日期(yyyy-MM-dd)
    - endMonth: 自定义时间(月为单位) -- 结束月份(yyyy-MM)
    - pageNum: 第几页
    - pageSize: 页数
    - recordType: 类型 1汇押货款、2 1:3押货退款申请、3新增信誉额、4超额押货款确认押货款、5无法识别款确认押货款、6扣减信誉额、7手工退押货款、8手工增加押货款、9转销售、10押货款还钱包欠款、11钱包款还押货欠款、12其它 13产品调价 14押货支付 15押货退货 16押货调整 17商城订单转押货额 18商城订单转押货额  19 押货保证金转移
    - remitType: 款项类型  1 ->汇押货款 2-> 退押货款  12 -> 其他  19->押货保证金转移
    - startDay: 自定义时间(天为单位) -- 开始日期(yyyy-MM-dd)
    - startMonth: 自定义时间(月为单位) -- 开始月份(yyyy-MM)
    - storeCode: 服务中心编号
    - type: 1 本月  2 上月   3 本年
    """

    url = "/appStore/store/inventory/mortgageAmount/remitDetailSearchList"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

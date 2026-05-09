import os

from util.client import client

data = {
    "bizNo": "",  # 业务单号
    "dbType": [],  # 19种底层款项类型 全部则为空  1汇押货款、2 1:3押货退款申请、3超额押货款退款、4超额押货款确认押货款、5无法识别款确认押货款、6无法识别款退款、7手工退押货款、8手工增加押货款、9转销售、10押货款还钱包欠款、11钱包款还押货欠款、12其它 13产品调价 14押货支付 15押货退货 16押货调整 17商城订单转押货额 18商城退货减押货额  19押货保证金转移 20->调整
    "endMonth": "",  # 结束月份期间(yyyy-MM)
    "pageNum": 0,  # 第几页
    "pageSize": 0,  # 页数
    "reportType": 0,  # 报表类型 0 -> 全部  1-> 汇/退押货款 2->调整金额  3-> 信誉额  14-> 押货使用  15-> 押货退货  17->配送返还  18 ->商城退货
    "sevenBankType": 0,  # 款项类型 0 -> 全部  1->汇押货款 2-> 1:3押货款退款申请  3-> 手工退押货款  4-> 手工增押货款  5-> 转销售  6->  钱包款与押货款互转 7-> 其他 、8->押货保证金转移
    "startMonth": "",  # 开始月份期间(yyyy-MM)
    "storeCode": "",  # 店铺编号
    "tenType": 0,  # 交易类型 0 -> 全部  1->汇押货款、2-> 退押货款、3-> 信誉额、9->扣减押货款、12-> 其他、13-> 产品调价、14-> 押货使用、15-> 押货退货、16-> 押货调整、17-> 配送返还、18-> 商城退货, 19->押货保证金转移 20->调整
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_inventory_mortgageAmount_listMortgageAmountRecord(data=data, headers=headers):
    """
    可用押货额变动变细
    /appStore/store/inventory/mortgageAmount/listMortgageAmountRecord

    参数说明:
    - bizNo: 业务单号
    - dbType: 19种底层款项类型 全部则为空  1汇押货款、2 1:3押货退款申请、3超额押货款退款、4超额押货款确认押货款、5无法识别款确认押货款、6无法识别款退款、7手工退押货款、8手工增加押货款、9转销售、10押货款还钱包欠款、11钱包款还押货欠款、12其它 13产品调价 14押货支付 15押货退货 16押货调整 17商城订单转押货额 18商城退货减押货额  19押货保证金转移 20->调整
    - endMonth: 结束月份期间(yyyy-MM)
    - pageNum: 第几页
    - pageSize: 页数
    - reportType: 报表类型 0 -> 全部  1-> 汇/退押货款 2->调整金额  3-> 信誉额  14-> 押货使用  15-> 押货退货  17->配送返还  18 ->商城退货
    - sevenBankType: 款项类型 0 -> 全部  1->汇押货款 2-> 1:3押货款退款申请  3-> 手工退押货款  4-> 手工增押货款  5-> 转销售  6->  钱包款与押货款互转 7-> 其他 、8->押货保证金转移
    - startMonth: 开始月份期间(yyyy-MM)
    - storeCode: 店铺编号
    - tenType: 交易类型 0 -> 全部  1->汇押货款、2-> 退押货款、3-> 信誉额、9->扣减押货款、12-> 其他、13-> 产品调价、14-> 押货使用、15-> 押货退货、16-> 押货调整、17-> 配送返还、18-> 商城退货, 19->押货保证金转移 20->调整
    """

    url = "/appStore/store/inventory/mortgageAmount/listMortgageAmountRecord"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

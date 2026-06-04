import os

from util.client import client

data = {
    "month": "",  # 月份 yyyy-MM
    "pageNum": 0,  # 第几页
    "pageSize": 0,  # 页数
    "recordType": 0,  #  空则为全部 款项类型 1汇押货款、2 1:3押货退款申请、3超额押货款退款、4超额押货款确认押货款、5无法识别款确认押货款、6无法识别款退款、7手工退押货款、8手工增加押货款、9转销售、10押货款还钱包欠款、11钱包款还押货欠款、12其它 13产品调价
    "storeCode": "",  # 服务中心编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_reportForm_storeRemitDetailPageList(data=data, headers=headers):
    """
    累计已汇押货款余额详情
    /mgmt/inventory/reportForm/storeRemitDetailPageList

    参数说明:
    - month: 月份 yyyy-MM
    - pageNum: 第几页
    - pageSize: 页数
    - recordType:  空则为全部 款项类型 1汇押货款、2 1:3押货退款申请、3超额押货款退款、4超额押货款确认押货款、5无法识别款确认押货款、6无法识别款退款、7手工退押货款、8手工增加押货款、9转销售、10押货款还钱包欠款、11钱包款还押货欠款、12其它 13产品调价
    - storeCode: 服务中心编号
    """

    url = "/mgmt/inventory/reportForm/storeRemitDetailPageList"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

import os

from util.client import client

params = {
    "bankName": "",  # 银行名称
    "companyCode": "",  # 分公司code
    "endMonth": 0,  # 结束月份(格式yyyyMM如202111)
    "id": 0,  # 主键id
    "pageNum": 0,  # 第几页
    "pageSize": 0,  # 页数
    "sourceType": 0,  # 款项类型  7手工退押货款、8手工增加押货款、9转销售、10押货款还钱包欠款、11钱包款还押货欠款、12其它
    "startMonth": 0,  # 开始月份(格式yyyyMM如202111)
    "storeCode": "",  # 店铺编号
    "verifyResult": 0,  # 审核结果  0未审核 1通过  2拒绝
    "verifyStatus": 0,  # 审核状态 0 待审核 1 已审核
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_remit_exportManualInputRemitList(params=params, headers=headers):
    """
    导出搜索数据Excel--手工录入
    /mgmt/inventory/remit/exportManualInputRemitList

    参数说明:
    - bankName: 银行名称
    - companyCode: 分公司code
    - endMonth: 结束月份(格式yyyyMM如202111)
    - id: 主键id
    - pageNum: 第几页
    - pageSize: 页数
    - sourceType: 款项类型  7手工退押货款、8手工增加押货款、9转销售、10押货款还钱包欠款、11钱包款还押货欠款、12其它
    - startMonth: 开始月份(格式yyyyMM如202111)
    - storeCode: 店铺编号
    - verifyResult: 审核结果  0未审核 1通过  2拒绝
    - verifyStatus: 审核状态 0 待审核 1 已审核
    """

    url = "/mgmt/inventory/remit/exportManualInputRemitList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

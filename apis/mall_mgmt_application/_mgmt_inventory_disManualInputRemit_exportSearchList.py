import os

from util.client import client

params = {
    "companyCode": "",  # 分公司code
    "endMonth": 0,  # 结束月份(格式yyyyMM如202111)
    "pageNum": 0,  # 第几页
    "pageSize": 0,  # 页数
    "payAccountBankName": "",  # 付款银行
    "sourceType": 0,  # 款项类型  3->其他、7->手工增加押货款、8->手工退押货款、9->押货保证金转移、24->转销售
    "startMonth": 0,  # 开始月份(格式yyyyMM如202111)
    "storeCode": "",  # 店铺编号
    "verifyResult": 0,  # 审核结果  0未审核 1通过  2拒绝
    "verifyStatus": 0,  # 审核状态 0 待审核 1 已审核
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_disManualInputRemit_exportSearchList(params=params, headers=headers):
    """
    85折手工录入流水搜索列表导出
    /mgmt/inventory/disManualInputRemit/exportSearchList

    参数说明:
    - companyCode: 分公司code
    - endMonth: 结束月份(格式yyyyMM如202111)
    - pageNum: 第几页
    - pageSize: 页数
    - payAccountBankName: 付款银行
    - sourceType: 款项类型  3->其他、7->手工增加押货款、8->手工退押货款、9->押货保证金转移、24->转销售
    - startMonth: 开始月份(格式yyyyMM如202111)
    - storeCode: 店铺编号
    - verifyResult: 审核结果  0未审核 1通过  2拒绝
    - verifyStatus: 审核状态 0 待审核 1 已审核
    """

    url = "/mgmt/inventory/disManualInputRemit/exportSearchList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

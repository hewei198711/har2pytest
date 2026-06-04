import os

from util.client import client

params = {
    "applyReason": "",  # 申请原因
    "auditStatus": "",  # 审核状态 1审核通过  2不通过 3待审核
    "companyCodes": [],  # 分公司编号列表
    "companyName": "",  # 分公司编号
    "endTime": "",  # 申请的结束时间
    "startTime": "",  # 申请的起始时间
    "storeCode": "",  # 服务中心编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_other_exportStoreOtherList(params=params, headers=headers):
    """
    批量导出其他申请记录
    /mgmt/store/other/exportStoreOtherList

    参数说明:
    - applyReason: 申请原因
    - auditStatus: 审核状态 1审核通过  2不通过 3待审核
    - companyCodes: 分公司编号列表
    - companyName: 分公司编号
    - endTime: 申请的结束时间
    - startTime: 申请的起始时间
    - storeCode: 服务中心编号
    """

    url = "/mgmt/store/other/exportStoreOtherList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

import os

from util.client import client

params = {
    "applyReason": "",  # 申请原因
    "auditStatus": 0,  # 审核状态：0->待审核;1->审核通过;2->驳回
    "companyCode": "",  # 分公司编号
    "companyCodes": [],  # 分公司编号列表
    "companyName": "",  # 分公司名称
    "endTime": "",  # 结束时间
    "pageNum": 0,  # 页码
    "pageSize": 0,  # 每页大小
    "startTime": "",  # 开始时间
    "storeStr": "",  # 服务中心编码或名称
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_store_certificate_list(params=params, headers=headers):
    """
    获取服务中心证件申请列表
    /mgmt/sys/store/certificate/list

    参数说明:
    - applyReason: 申请原因
    - auditStatus: 审核状态：0->待审核;1->审核通过;2->驳回
    - companyCode: 分公司编号
    - companyCodes: 分公司编号列表
    - companyName: 分公司名称
    - endTime: 结束时间
    - pageNum: 页码
    - pageSize: 每页大小
    - startTime: 开始时间
    - storeStr: 服务中心编码或名称
    """

    url = "/mgmt/sys/store/certificate/list"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

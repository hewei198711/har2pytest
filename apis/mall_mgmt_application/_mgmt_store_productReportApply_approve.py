import os

from util.client import client

data = {
    "approveOpinion": "",  # 审批意见
    "id": 0,  # 主键id
    "status": 0,  # 1审核通过 2已驳回
    "validitDate": "",  # 下载有效期(yyyy-MM-dd)
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_productReportApply_approve(data=data, headers=headers):
    """
    运营后台:成品报告申请审批
    /mgmt/store/productReportApply/approve

    参数说明:
    - approveOpinion: 审批意见
    - id: 主键id
    - status: 1审核通过 2已驳回
    - validitDate: 下载有效期(yyyy-MM-dd)
    """

    url = "/mgmt/store/productReportApply/approve"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

import os

from util.client import client

data = {
    "companyCodes": [],  # 分公司编号列表
    "companyName": "",  # 分公司编号
    "pageNum": 0,  # 当前页,默认第1页
    "pageSize": 0,  # 每页显示数,默认10条
    "storeCode": "",  # 店铺编号
    "verifyStatus": "",  # 审核状态 1待审核 2审核通过 3已驳回 4已完成 5已撤销 6完成待受理 7撤销待受理
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_graduation_queryGraduationList(data=data, headers=headers):
    """
    结业申请列表--后台
    /mgmt/store/graduation/queryGraduationList

    参数说明:
    - companyCodes: 分公司编号列表
    - companyName: 分公司编号
    - pageNum: 当前页,默认第1页
    - pageSize: 每页显示数,默认10条
    - storeCode: 店铺编号
    - verifyStatus: 审核状态 1待审核 2审核通过 3已驳回 4已完成 5已撤销 6完成待受理 7撤销待受理
    """

    url = "/mgmt/store/graduation/queryGraduationList"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

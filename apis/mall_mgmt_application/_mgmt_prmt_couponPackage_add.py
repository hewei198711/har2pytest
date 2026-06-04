import os

from util.client import client

data = {
    "couponId": 0,  # 优惠券id
    "grantTime": "",  # 定时派发时间
    "grantType": 0,  # 券包派发类型：1-即时派发,2-定时派发,3-对接外部系统
    "id": 0,  # 主键id
    "importKey": "",  # 导入操作键
    "remark": "",  # 派发说明
    "state": 0,  # 券包派发状态：1-待审核,2-派发中,3-已完成,4-已驳回,5-草稿,6-已停止
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_couponPackage_add(data=data, headers=headers):
    """
    新建派发任务
    /mgmt/prmt/couponPackage/add

    参数说明:
    - couponId: 优惠券id
    - grantTime: 定时派发时间
    - grantType: 券包派发类型：1-即时派发,2-定时派发,3-对接外部系统
    - id: 主键id
    - importKey: 导入操作键
    - remark: 派发说明
    - state: 券包派发状态：1-待审核,2-派发中,3-已完成,4-已驳回,5-草稿,6-已停止
    """

    url = "/mgmt/prmt/couponPackage/add"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

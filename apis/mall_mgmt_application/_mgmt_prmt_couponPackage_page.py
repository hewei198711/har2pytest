import os

from util.client import client

params = {
    "couponName": "",  # 优惠券名称
    "couponNumber": "",  # 优惠券编码
    "createTimeEnd": "",  # 创建时间止 格式：yyyy-MM-dd HH:mm:ss
    "createTimeStart": "",  # 创建时间起 格式：yyyy-MM-dd HH:mm:ss
    "grantTimeEnd": "",  # 派发时间止 格式：yyyy-MM-dd HH:mm:ss
    "grantTimeStart": "",  # 派发时间起 格式：yyyy-MM-dd HH:mm:ss
    "grantType": 0,  # 券包派发类型：1-即时派发,2-定时派发,3-对接外部系统
    "pageNum": 0,  # 当前页
    "pageSize": 0,  # 每页数量
    "state": 0,  # 券包派发状态：1-待审核,2-派发中,3-已完成,4-已驳回,5-草稿,6-已停止
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_couponPackage_page(params=params, headers=headers):
    """
    分页查询派发任务
    /mgmt/prmt/couponPackage/page

    参数说明:
    - couponName: 优惠券名称
    - couponNumber: 优惠券编码
    - createTimeEnd: 创建时间止 格式：yyyy-MM-dd HH:mm:ss
    - createTimeStart: 创建时间起 格式：yyyy-MM-dd HH:mm:ss
    - grantTimeEnd: 派发时间止 格式：yyyy-MM-dd HH:mm:ss
    - grantTimeStart: 派发时间起 格式：yyyy-MM-dd HH:mm:ss
    - grantType: 券包派发类型：1-即时派发,2-定时派发,3-对接外部系统
    - pageNum: 当前页
    - pageSize: 每页数量
    - state: 券包派发状态：1-待审核,2-派发中,3-已完成,4-已驳回,5-草稿,6-已停止
    """

    url = "/mgmt/prmt/couponPackage/page"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

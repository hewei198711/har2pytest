import os

from util.client import client

params = {
    "beginDate": "",  # 开始时间, 格式：yyyy-MM-dd
    "endDate": "",  # 结束时间, 格式：yyyy-MM-dd
    "pageNum": 0,  # 第几页
    "pageSize": 0,  # 每页显示页数
    "profileChangeType": 0,  # 变更类型，1/变更负责人手机号, 2/变更配偶手机号，9/负责人联系地址, 10/微信号
    "storeCode": "",  # 服务中心编号（店铺系统可不传）
    "submitter": "",  # 修改人
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_profile_getLeaderChangeList(params=params, headers=headers):
    """
    获取负责人变更记录列表
    /appStore/store/profile/getLeaderChangeList

    参数说明:
    - beginDate: 开始时间, 格式：yyyy-MM-dd
    - endDate: 结束时间, 格式：yyyy-MM-dd
    - pageNum: 第几页
    - pageSize: 每页显示页数
    - profileChangeType: 变更类型，1/变更负责人手机号, 2/变更配偶手机号，9/负责人联系地址, 10/微信号
    - storeCode: 服务中心编号（店铺系统可不传）
    - submitter: 修改人
    """

    url = "/appStore/store/profile/getLeaderChangeList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

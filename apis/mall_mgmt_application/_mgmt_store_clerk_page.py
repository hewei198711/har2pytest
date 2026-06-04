import os

from util.client import client

params = {
    "createEndDate": "",  # 创建结束日期，格式：yyyy-MM-dd
    "createStartDate": "",  # 创建开始日期，格式：yyyy-MM-dd
    "id": 0,  # 店员ID
    "mobile": "",  # 手机
    "name": "",  # 姓名
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 每页显示数
    "storeCode": "",  # 服务中心编号（门店系统不需要传）
    "username": "",  # 用户账号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_clerk_page(params=params, headers=headers):
    """
    查询店员列表
    /mgmt/store/clerk/page

    参数说明:
    - createEndDate: 创建结束日期，格式：yyyy-MM-dd
    - createStartDate: 创建开始日期，格式：yyyy-MM-dd
    - id: 店员ID
    - mobile: 手机
    - name: 姓名
    - pageNum: 页数
    - pageSize: 每页显示数
    - storeCode: 服务中心编号（门店系统不需要传）
    - username: 用户账号
    """

    url = "/mgmt/store/clerk/page"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

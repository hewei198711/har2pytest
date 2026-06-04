import os

from util.client import client

params = {
    "grantId": 0,  # 优惠券包派发任务id
    "memberCard": "",  # 派发用户卡号
    "memberName": "",  # 派发用户姓名
    "packNumber": "",  # 券包编码
    "pageNum": 0,  # 当前页
    "pageSize": 0,  # 每页数量
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_couponPackage_exportPagePack(params=params, headers=headers):
    """
    导出优惠券券包列表数据明细
    /mgmt/prmt/couponPackage/exportPagePack

    参数说明:
    - grantId: 优惠券包派发任务id
    - memberCard: 派发用户卡号
    - memberName: 派发用户姓名
    - packNumber: 券包编码
    - pageNum: 当前页
    - pageSize: 每页数量
    """

    url = "/mgmt/prmt/couponPackage/exportPagePack"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

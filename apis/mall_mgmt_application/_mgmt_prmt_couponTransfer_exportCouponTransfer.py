import os

from util.client import client

params = {
    "cardNo": "",  # 会员卡号
    "code": "",  # 门店编号
    "grantId": 0,  # 派发id
    "mobile": "",  # 手机号码
    "pageNum": 0,  # 当前页
    "pageSize": 0,  # 每页条数
    "realName": "",  # 真实姓名
    "state": 0,  # 使用状态1未使用2已使用3已作废4已失效5占用中
    "transferType": 0,  # 转赠方式1指定用户2扫码领取3转发领取
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_couponTransfer_exportCouponTransfer(params=params, headers=headers):
    """
    导出转赠优惠券(详情)
    /mgmt/prmt/couponTransfer/exportCouponTransfer

    参数说明:
    - cardNo: 会员卡号
    - code: 门店编号
    - grantId: 派发id
    - mobile: 手机号码
    - pageNum: 当前页
    - pageSize: 每页条数
    - realName: 真实姓名
    - state: 使用状态1未使用2已使用3已作废4已失效5占用中
    - transferType: 转赠方式1指定用户2扫码领取3转发领取
    """

    url = "/mgmt/prmt/couponTransfer/exportCouponTransfer"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

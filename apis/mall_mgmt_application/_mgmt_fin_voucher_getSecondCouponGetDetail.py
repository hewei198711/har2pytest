import os

from util.client import client

data = {
    "cardNo": "",  # 会员卡号
    "couponStatus": 0,  # 券状态
    "couponStatusList": [],  # 券状态集合
    "from": 0,  # TODO: 添加参数说明
    "getEndTime": "",  # 获券结束时间-yyyy-MM-dd HH:mm:ss
    "getStartTime": "",  # 获券开始时间-yyyy-MM-dd HH:mm:ss
    "getType": 0,  # 交易类型，1：购物获得；2：月结更新
    "memberType": 0,  # 顾客类型
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 每页显示数
    "sourceOrderNo": "",  # 来源订单号
    "sourceStoreCode": "",  # 服务中心编号
    "transMonth": "",  # 交易月份YYYYMM，商城使用
    "transMonthEnd": "",  # 交易月份结束YYYYMM，运营后台使用
    "transMonthStart": "",  # 交易月份开始YYYYMM，运营后台使用
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_fin_voucher_getSecondCouponGetDetail(data=data, headers=headers):
    """
    秒返券获券明细
    /mgmt/fin/voucher/getSecondCouponGetDetail

    参数说明:
    - cardNo: 会员卡号
    - couponStatus: 券状态
    - couponStatusList: 券状态集合
    - getEndTime: 获券结束时间-yyyy-MM-dd HH:mm:ss
    - getStartTime: 获券开始时间-yyyy-MM-dd HH:mm:ss
    - getType: 交易类型，1：购物获得；2：月结更新
    - memberType: 顾客类型
    - pageNum: 页数
    - pageSize: 每页显示数
    - sourceOrderNo: 来源订单号
    - sourceStoreCode: 服务中心编号
    - transMonth: 交易月份YYYYMM，商城使用
    - transMonthEnd: 交易月份结束YYYYMM，运营后台使用
    - transMonthStart: 交易月份开始YYYYMM，运营后台使用
    """

    url = "/mgmt/fin/voucher/getSecondCouponGetDetail"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

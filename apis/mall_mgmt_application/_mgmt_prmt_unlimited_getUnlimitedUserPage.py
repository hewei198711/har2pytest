import os

from util.client import client

params = {
    "cardNo": "",  # 会员卡号
    "importKey": "",  # 导入操作键
    "independentLimit": 0,  # 自定义独立限量1:开启;0:关闭
    "limitNumber": 0,  # 限制购买个数-1不限-2按需分配
    "limitType": 0,  # 限购方式1不限量2独立限量3统一限量4按需导入5按PV阶梯配置
    "memberState": 0,  # 状态1启用2禁用中
    "mobile": "",  # 手机号
    "pageNum": 0,  # 当前页
    "pageSize": 0,  # 每页条数
    "promotionId": 0,  # 活动id
    "purchasedCount": 0,  # 已购买数量
    "realName": "",  # 会员姓名
    "serialNo": "",  # 商品编码
    "totalCount": 0,  # 可购买数量
    "updateTimeMax": "",  # 修改时间大
    "updateTimeMin": "",  # 修改时间小
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_unlimited_getUnlimitedUserPage(params=params, headers=headers):
    """
    不受限制活动顾客分页列表
    /mgmt/prmt/unlimited/getUnlimitedUserPage

    参数说明:
    - cardNo: 会员卡号
    - importKey: 导入操作键
    - independentLimit: 自定义独立限量1:开启;0:关闭
    - limitNumber: 限制购买个数-1不限-2按需分配
    - limitType: 限购方式1不限量2独立限量3统一限量4按需导入5按PV阶梯配置
    - memberState: 状态1启用2禁用中
    - mobile: 手机号
    - pageNum: 当前页
    - pageSize: 每页条数
    - promotionId: 活动id
    - purchasedCount: 已购买数量
    - realName: 会员姓名
    - serialNo: 商品编码
    - totalCount: 可购买数量
    - updateTimeMax: 修改时间大
    - updateTimeMin: 修改时间小
    """

    url = "/mgmt/prmt/unlimited/getUnlimitedUserPage"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

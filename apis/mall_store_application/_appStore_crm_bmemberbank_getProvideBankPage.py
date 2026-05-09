import os

from util.client import client

data = {
    "cardNo": "",  # 会员卡号
    "channel": 0,  # 开通渠道：1->H5；2->APP；3->小程序；4->PC；5->填表；6->上海健康；7->油葱极速版
    "createEndTimeLong": 0,  # 创建/绑定结束时间
    "createStartTimeLong": 0,  # 创建/绑定开始时间
    "mobile": "",  # 手机号
    "pageNum": 0,  # 当前页码
    "pageSize": 0,  # 每页条数
    "platform": 0,  # 1、商城运营后台平台,2、店铺运营平台或者app服务中心平台
    "provideType": 0,  # 发放类型：1->直销员；2->客户经理
    "realname": "",  # 姓名
    "status": 0,  # 银行卡状态 1->正常；2->汇退；3->删除
    "storeCode": "",  # 服务中心编码
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _appStore_crm_bmemberbank_getProvideBankPage(data=data, headers=headers):
    """
    会员发放银行卡管理列表查询-店铺运营端
    /appStore/crm/bmemberbank/getProvideBankPage

    参数说明:
    - cardNo: 会员卡号
    - channel: 开通渠道：1->H5；2->APP；3->小程序；4->PC；5->填表；6->上海健康；7->油葱极速版
    - createEndTimeLong: 创建/绑定结束时间
    - createStartTimeLong: 创建/绑定开始时间
    - mobile: 手机号
    - pageNum: 当前页码
    - pageSize: 每页条数
    - platform: 1、商城运营后台平台,2、店铺运营平台或者app服务中心平台
    - provideType: 发放类型：1->直销员；2->客户经理
    - realname: 姓名
    - status: 银行卡状态 1->正常；2->汇退；3->删除
    - storeCode: 服务中心编码
    """

    url = "/appStore/crm/bmemberbank/getProvideBankPage"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

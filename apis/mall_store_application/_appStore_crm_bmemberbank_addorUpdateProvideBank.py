import os

from util.client import client

data = {
    "bankNo": "",  # 银行卡号
    "bankOpenName": "",  # 开户银行名称
    "bankOpenType": "",  # 开户银行类型
    "cardNo": "",  # 会员卡号
    "channel": "",  # PC,APP
    "city": "",  # 地址市
    "createTime": "",  # 创建时间
    "district": "",  # 地址区
    "id": 0,  # id
    "memberId": 0,  # 用户id
    "mobile": "",  # 手机号
    "opertstatus": 0,  # 操作类型
    "platform": 0,  # 代邦银行卡平台,1、商城运营后台平台,2、店铺运营平台,3、app服务中心平台,4、油葱极速版
    "provideType": 0,  # 发放类型：1->直销员；2->客户经理
    "province": "",  # 地址省份
    "realname": "",  # 姓名
    "source": 0,  # 来源.1系统登录操作, 2其他地方来的数据
    "status": 0,  # 银行卡状态 1->汇退；2->正常；3->无账号
    "updateTime": "",  # 最后一次信息变更时间
    "updaterId": 0,  # 更新人ID，留空就是自己，有ID就是操作员ID
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _appStore_crm_bmemberbank_addorUpdateProvideBank(data=data, headers=headers):
    """
    新增或修改会员发放银行卡
    /appStore/crm/bmemberbank/addorUpdateProvideBank

    参数说明:
    - bankNo: 银行卡号
    - bankOpenName: 开户银行名称
    - bankOpenType: 开户银行类型
    - cardNo: 会员卡号
    - channel: PC,APP
    - city: 地址市
    - createTime: 创建时间
    - district: 地址区
    - id: id
    - memberId: 用户id
    - mobile: 手机号
    - opertstatus: 操作类型
    - platform: 代邦银行卡平台,1、商城运营后台平台,2、店铺运营平台,3、app服务中心平台,4、油葱极速版
    - provideType: 发放类型：1->直销员；2->客户经理
    - province: 地址省份
    - realname: 姓名
    - source: 来源.1系统登录操作, 2其他地方来的数据
    - status: 银行卡状态 1->汇退；2->正常；3->无账号
    - updateTime: 最后一次信息变更时间
    - updaterId: 更新人ID，留空就是自己，有ID就是操作员ID
    """

    url = "/appStore/crm/bmemberbank/addorUpdateProvideBank"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

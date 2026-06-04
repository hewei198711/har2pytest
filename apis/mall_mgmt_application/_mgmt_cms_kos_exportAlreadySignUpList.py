import os

from util.client import client

data = {
    "cardNo": "",  # 会员卡号
    "channelsId": "",  # 视频号id
    "channelsName": "",  # 视频号名称
    "companyCode": "",  # 所属分公司编号
    "isAgentChildren": 0,  # 是否经销商子女: 1.是 0.否
    "isChannelsHolder": 0,  # 是否有视频号: 1.是 0.否
    "isExport": False,  # TODO: 添加参数说明
    "loginChannel": 0,  # 登录端: 1.APP 2.小程序
    "loginIdentity": 0,  # 登录身份: 1.主卡 2.配偶 3.子账号
    "loginMobile": "",  # 登陆手机号
    "memberType": 0,  # 顾客身份: 1.会员 2.VIP会员 3.云商 4.微店
    "modifyTimesOfMonth": "",  # 1个自然月剩余修改次数
    "modifyTimesOfMonthInt": 0,  # TODO: 添加参数说明
    "modifyTimesOfYear": "",  # 12个自然月剩余修改次数
    "modifyTimesOfYearInt": 0,  # TODO: 添加参数说明
    "pageNum": 0,  # 页码
    "pageSize": 0,  # 每页页数
    "parentCardNo": "",  # 父母卡号
    "parentMobile": "",  # 父母手机号
    "parentUserName": "",  # 父母姓名
    "signUpTimeQueryEnd": "",  # 报名时间查询结束时间
    "signUpTimeQueryStart": "",  # 报名时间查询开始时间
    "storeCode": "",  # 服务中心编号
    "userName": "",  # 姓名
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_kos_exportAlreadySignUpList(data=data, headers=headers):
    """
    导出已报名人员名单列表
    /mgmt/cms/kos/exportAlreadySignUpList

    参数说明:
    - cardNo: 会员卡号
    - channelsId: 视频号id
    - channelsName: 视频号名称
    - companyCode: 所属分公司编号
    - isAgentChildren: 是否经销商子女: 1.是 0.否
    - isChannelsHolder: 是否有视频号: 1.是 0.否
    - loginChannel: 登录端: 1.APP 2.小程序
    - loginIdentity: 登录身份: 1.主卡 2.配偶 3.子账号
    - loginMobile: 登陆手机号
    - memberType: 顾客身份: 1.会员 2.VIP会员 3.云商 4.微店
    - modifyTimesOfMonth: 1个自然月剩余修改次数
    - modifyTimesOfYear: 12个自然月剩余修改次数
    - pageNum: 页码
    - pageSize: 每页页数
    - parentCardNo: 父母卡号
    - parentMobile: 父母手机号
    - parentUserName: 父母姓名
    - signUpTimeQueryEnd: 报名时间查询结束时间
    - signUpTimeQueryStart: 报名时间查询开始时间
    - storeCode: 服务中心编号
    - userName: 姓名
    """

    url = "/mgmt/cms/kos/exportAlreadySignUpList"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

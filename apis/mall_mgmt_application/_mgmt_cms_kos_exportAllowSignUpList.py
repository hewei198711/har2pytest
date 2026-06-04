import os

from util.client import client

data = {
    "cardNo": "",  # 会员卡号
    "companyCode": "",  # 所属分公司编号
    "gender": 0,  # 性别: 1.男 2.女
    "identity": 0,  # 身份: 1.主卡 2.配偶 3.子账号
    "isExport": False,  # TODO: 添加参数说明
    "isSignUp": 0,  # 是否已报名: 1.是 0.否
    "mobile": "",  # 注册手机号
    "pageNum": 0,  # 页码
    "pageSize": 0,  # 每页页数
    "qualifiedMonthQueryEnd": "",  # 达标月份查询结束时间
    "qualifiedMonthQueryStart": "",  # 达标月份查询开始时间
    "userName": "",  # 姓名
    "userType": 0,  # 类型: 1.店主 2.经销商 3.轻创 4.经销商子女
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_kos_exportAllowSignUpList(data=data, headers=headers):
    """
    导出可报名人员名单列表
    /mgmt/cms/kos/exportAllowSignUpList

    参数说明:
    - cardNo: 会员卡号
    - companyCode: 所属分公司编号
    - gender: 性别: 1.男 2.女
    - identity: 身份: 1.主卡 2.配偶 3.子账号
    - isSignUp: 是否已报名: 1.是 0.否
    - mobile: 注册手机号
    - pageNum: 页码
    - pageSize: 每页页数
    - qualifiedMonthQueryEnd: 达标月份查询结束时间
    - qualifiedMonthQueryStart: 达标月份查询开始时间
    - userName: 姓名
    - userType: 类型: 1.店主 2.经销商 3.轻创 4.经销商子女
    """

    url = "/mgmt/cms/kos/exportAllowSignUpList"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

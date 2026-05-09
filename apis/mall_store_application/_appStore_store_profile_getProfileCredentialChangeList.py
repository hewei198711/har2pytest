import os

from util.client import client

params = {
    "changeType": 0,  # 变更类型，手机号变更类型时必填，1/变更负责人手机号, 2/变更配偶手机号, 3/变更服务中心电话, 4/变更收货地址, 5/变更证件信息, 6/新增银行账户, 7/修改银行账户, 8/废除银行账户, 9/负责人联系地址，10/微信号，11/电子印章信息变更，12/电子印章(个人)信息变更
    "changeTypes": "",  # 变更类型数组，用逗号分隔
    "companyCode": "",  # 分公司编号
    "companyCodes": [],  # 分公司编号列表
    "endDate": "",  # 申请结束日期，格式：yyyy-MM-dd
    "id": 0,  # 资料变更ID
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 每页显示数
    "startDate": "",  # 申请开始日期，格式：yyyy-MM-dd
    "storeCode": "",  # 服务中心编码(门店系统不需要传)
    "storeName": "",  # 服务中心名称或者编号
    "submitter": "",  # 提交人/修改人
    "verifyStatus": 0,  # 审核状态, 1/审核通过, 2/审核不通过, 3/待审核, 4/已取消
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_profile_getProfileCredentialChangeList(params=params, headers=headers):
    """
    获取服务中心证件信息变更列表
    /appStore/store/profile/getProfileCredentialChangeList

    参数说明:
    - changeType: 变更类型，手机号变更类型时必填，1/变更负责人手机号, 2/变更配偶手机号, 3/变更服务中心电话, 4/变更收货地址, 5/变更证件信息, 6/新增银行账户, 7/修改银行账户, 8/废除银行账户, 9/负责人联系地址，10/微信号，11/电子印章信息变更，12/电子印章(个人)信息变更
    - changeTypes: 变更类型数组，用逗号分隔
    - companyCode: 分公司编号
    - companyCodes: 分公司编号列表
    - endDate: 申请结束日期，格式：yyyy-MM-dd
    - id: 资料变更ID
    - pageNum: 页数
    - pageSize: 每页显示数
    - startDate: 申请开始日期，格式：yyyy-MM-dd
    - storeCode: 服务中心编码(门店系统不需要传)
    - storeName: 服务中心名称或者编号
    - submitter: 提交人/修改人
    - verifyStatus: 审核状态, 1/审核通过, 2/审核不通过, 3/待审核, 4/已取消
    """

    url = "/appStore/store/profile/getProfileCredentialChangeList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

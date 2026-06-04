import os

from util.client import client

data = {
    "companyCode": "",  # 分公司编号
    "companyCodeList": [],  # 分公司编号列表
    "companySignEndDate": "",  # 公司签署结束时间(yyyy-MM-dd HH:mm:ss)
    "companySignStartDate": "",  # 公司签署开始时间(yyyy-MM-dd HH:mm:ss)
    "contractType": 0,  # 合同类型，1/经营合同，2/协议
    "customerType": 0,  # 客户类型：1/服务中心，2/服务公司，3/个人
    "customerTypeList": "",  # 客户类型集合
    "endCommitTime": "",  # 提交日期结束时间(yyyy-MM-dd)
    "expireEndDate": "",  # 签署结束有效期
    "expireStartDate": "",  # 签署开始有效期
    "ids": [],  # 提交合同的主键id。选中，必传该字段；未选中，不能传
    "isExport": False,  # 是否导出，默认非导出
    "leaderNo": "",  # 负责人卡号
    "memberCardNo": "",  # 用户会员卡号
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 每页显示数
    "remark": "",  # 备注
    "signStatus": 0,  # 签署状态，0.未生成，1.未提交，2.待店铺签署，3.待公司签署，4.已完成，5.已撤销，6，生成失败，7.拒签，8.待审批(线下)，9.已驳回（线下），10.已完成（线下），11.待用户签署
    "signStatusList": [],  # 签署状态集合
    "signType": 0,  # 签署类型：1/单方签署，2/双方签署，3/三方签署
    "startCommitTime": "",  # 提交日期开始时间(yyyy-MM-dd)
    "storeCode": "",  # 服务中心编号
    "storeSignEndDate": "",  # 店铺签署结束时间(yyyy-MM-dd HH:mm:ss)
    "storeSignStartDate": "",  # 店铺签署开始时间(yyyy-MM-dd HH:mm:ss)
    "templateName": "",  # 合同模板名称
    "templateNo": "",  # 合同模板编号
    "year": "",  # 年度
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_exportContractList(data=data, headers=headers):
    """
    导出合同信息excel
    /mgmt/store/exportContractList

    参数说明:
    - companyCode: 分公司编号
    - companyCodeList: 分公司编号列表
    - companySignEndDate: 公司签署结束时间(yyyy-MM-dd HH:mm:ss)
    - companySignStartDate: 公司签署开始时间(yyyy-MM-dd HH:mm:ss)
    - contractType: 合同类型，1/经营合同，2/协议
    - customerType: 客户类型：1/服务中心，2/服务公司，3/个人
    - customerTypeList: 客户类型集合
    - endCommitTime: 提交日期结束时间(yyyy-MM-dd)
    - expireEndDate: 签署结束有效期
    - expireStartDate: 签署开始有效期
    - ids: 提交合同的主键id。选中，必传该字段；未选中，不能传
    - isExport: 是否导出，默认非导出
    - leaderNo: 负责人卡号
    - memberCardNo: 用户会员卡号
    - pageNum: 页数
    - pageSize: 每页显示数
    - remark: 备注
    - signStatus: 签署状态，0.未生成，1.未提交，2.待店铺签署，3.待公司签署，4.已完成，5.已撤销，6，生成失败，7.拒签，8.待审批(线下)，9.已驳回（线下），10.已完成（线下），11.待用户签署
    - signStatusList: 签署状态集合
    - signType: 签署类型：1/单方签署，2/双方签署，3/三方签署
    - startCommitTime: 提交日期开始时间(yyyy-MM-dd)
    - storeCode: 服务中心编号
    - storeSignEndDate: 店铺签署结束时间(yyyy-MM-dd HH:mm:ss)
    - storeSignStartDate: 店铺签署开始时间(yyyy-MM-dd HH:mm:ss)
    - templateName: 合同模板名称
    - templateNo: 合同模板编号
    - year: 年度
    """

    url = "/mgmt/store/exportContractList"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

import os

from util.client import client

data = {
    "applySheetUrl": "",  # 申请表url，多个用逗号隔开
    "code": "",  # 验证码
    "companyCode": "",  # 所属分公司编号
    "companyName": "",  # 所属分公司名称
    "dispenserHandling": "",  # 未领取的水机售后处理方式 '1'完成水机顾客信息 '2'放弃处理 '3'无水机信息 '4'转店
    "dispenserMoveStorecode": "",  # 未领取水机转店服务中心编号
    "graduationReason": 0,  # 结业原因 '1'选址困难 '2'无精力照看店铺 '3'收支不足以店内开支 '4'其他
    "graduationReasonOther": "",  # 其他结业原因
    "inventoryHandling": "",  # 押货库存处理方式
    "inventoryMoveStorecode": "",  # 压货库存转店服务中心编号
    "oldSysHandling": "",  # 旧系统库存处理方式
    "oldSysMoveStorecode": "",  # 旧系统库存转店服务中心编号
    "phoneNo": "",  # 手机号码
    "port": 0,  # 请求端 0后台 1APP 2PC
    "storeCode": "",  # 店铺编号
    "storeName": "",  # 服务中心名称
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _appStore_appAndPc_store_graduation_addGraduationApply(data=data, headers=headers):
    """
    添加结业申请--web,app
    /appStore/appAndPc/store/graduation/addGraduationApply

    参数说明:
    - applySheetUrl: 申请表url，多个用逗号隔开
    - code: 验证码
    - companyCode: 所属分公司编号
    - companyName: 所属分公司名称
    - dispenserHandling: 未领取的水机售后处理方式 '1'完成水机顾客信息 '2'放弃处理 '3'无水机信息 '4'转店
    - dispenserMoveStorecode: 未领取水机转店服务中心编号
    - graduationReason: 结业原因 '1'选址困难 '2'无精力照看店铺 '3'收支不足以店内开支 '4'其他
    - graduationReasonOther: 其他结业原因
    - inventoryHandling: 押货库存处理方式
    - inventoryMoveStorecode: 压货库存转店服务中心编号
    - oldSysHandling: 旧系统库存处理方式
    - oldSysMoveStorecode: 旧系统库存转店服务中心编号
    - phoneNo: 手机号码
    - port: 请求端 0后台 1APP 2PC
    - storeCode: 店铺编号
    - storeName: 服务中心名称
    """

    url = "/appStore/appAndPc/store/graduation/addGraduationApply"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

import os

from util.client import client

data = {
    "cardVOs": [
        {
            "address": "",
            "addressDetail": "",
            "applyId": 0,
            "createTime": "",
            "del": 0,
            "effectTerm": "",
            "gender": "",
            "id": 0,
            "idCardFmPic": "",
            "idCardNo": "",
            "idCardZmPic": "",
            "identityCardType": 0,
            "isLongTime": 0,
            "issuingAuthority": "",
            "licenceType": 0,
            "name": "",
            "storeCode": "",
        }
    ],  # 身份证年审pojo
    "companyCode": "",  # 分公司code
    "id": 0,  # 主键id(编辑时需要)
    "licenseVOs": [
        {
            "applyId": 0,
            "businessFw": "",
            "businessType": "",
            "bzTime": "",
            "createTime": "",
            "del": 0,
            "effectTerm": "",
            "id": 0,
            "isLongTime": 0,
            "issuingAuthority": "",
            "legalPerson": "",
            "licenceName": "",
            "licencePic": "",
            "licenceType": 0,
            "name": "",
            "otherPic": "",
            "storeCode": "",
            "zcNo": "",
        }
    ],  # 证件年审pojo
    "personImageVO": {
        "applyId": 0,
        "createTime": "",
        "del": 0,
        "id": 0,
        "imagePic": "",
        "spousePic": "",
        "storeCode": "",
    },  # 个人形象年审pojo
    "reviewModelName": "",  # 年审类型(模块)名称 身份证年审、证件年审、店铺形象年审、个人形象年审
    "reviewModelType": 0,  # 年审类型(模块) 1-身份证年审、2-证件年审、3-店铺形象年审、4-个人形象年审
    "reviewTitle": "",  # 身份证年审、证件年审、店铺形象年审、个人形象年审
    "storeCode": "",  # 服务中心编号
    "storeImageVO": {
        "applyId": 0,
        "bjqPic": "",
        "createTime": "",
        "del": 0,
        "facadePic": "",
        "id": 0,
        "productTyA": "",
        "productTyB": "",
        "storeCode": "",
        "storeVedio": "",
    },  # 店铺信息年审pojo
    "storeName": "",  # 服务中心名称
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_commitOrEdit(data=data, headers=headers):
    """
    年审申请提交
    /appStore/store/commitOrEdit

    参数说明:
    - cardVOs: 身份证年审pojo
    - cardVOs.address: address
    - cardVOs.addressDetail: 详细地址
    - cardVOs.applyId: 申请id
    - cardVOs.createTime: create_time
    - cardVOs.del: del
    - cardVOs.effectTerm: 有效期
    - cardVOs.gender: 性别
    - cardVOs.idCardFmPic: 反面照片地址
    - cardVOs.idCardNo: 身份证号
    - cardVOs.idCardZmPic: 正面照片地址
    - cardVOs.identityCardType: 身份证类型  1身份证 2其他证件
    - cardVOs.isLongTime:  是否长期  0 是  1 否
    - cardVOs.issuingAuthority: 发证机关
    - cardVOs.licenceType: 证件类型  1 法人 2负责人 3 配偶
    - cardVOs.name: 姓名
    - cardVOs.storeCode: 服务中心编号
    - companyCode: 分公司code
    - id: 主键id(编辑时需要)
    - licenseVOs: 证件年审pojo
    - licenseVOs.applyId: 申请id
    - licenseVOs.businessFw: 经营范围
    - licenseVOs.businessType: 经营类型
    - licenseVOs.bzTime: 办证日期
    - licenseVOs.createTime: create_time
    - licenseVOs.del: del
    - licenseVOs.effectTerm: 有效期 “~” 隔开两日期
    - licenseVOs.id: id
    - licenseVOs.isLongTime:  是否长期  0 否 1 是
    - licenseVOs.issuingAuthority: 发证机关
    - licenseVOs.legalPerson: 法人
    - licenseVOs.licenceName: 证件名称
    - licenseVOs.licencePic: 营业执照
    - licenseVOs.licenceType: 证件类型  1 营业执照 2食品经营许可证
    - licenseVOs.name: 名称
    - licenseVOs.otherPic: 其他照片
    - licenseVOs.storeCode: 服务中心编号
    - licenseVOs.zcNo: 注册号
    - personImageVO: 个人形象年审pojo
    - personImageVO.applyId: 申请id
    - personImageVO.createTime: create_time
    - personImageVO.del: del
    - personImageVO.imagePic: 个人形象照片,多张逗号隔开
    - personImageVO.spousePic: 配偶形象照片,多张逗号隔开
    - personImageVO.storeCode: store_code
    - reviewModelName: 年审类型(模块)名称 身份证年审、证件年审、店铺形象年审、个人形象年审
    - reviewModelType: 年审类型(模块) 1-身份证年审、2-证件年审、3-店铺形象年审、4-个人形象年审
    - reviewTitle: 身份证年审、证件年审、店铺形象年审、个人形象年审
    - storeCode: 服务中心编号
    - storeImageVO: 店铺信息年审pojo
    - storeImageVO.applyId: 申请id
    - storeImageVO.bjqPic: 背景墙照片
    - storeImageVO.createTime: create_time
    - storeImageVO.facadePic: 门面照片
    - storeImageVO.id: id
    - storeImageVO.productTyA: 产品体验A区
    - storeImageVO.productTyB: 产品体验B区
    - storeImageVO.storeCode: 服务中心编号
    - storeImageVO.storeVedio: 店铺视频
    - storeName: 服务中心名称
    """

    url = "/appStore/store/commitOrEdit"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

import os

from util.client import client

data = {
    "activityId": 0,  # 抽奖活动id
    "concluding": "",  # 结束语
    "deviceLimit": 0,  # 设备答题限制 0.否 1.是
    "deviceRefillLimit": 0,  # 每个设备的答题限制次数
    "displayType": 0,  # 发布对象类型: 0:所有用户 1:标签用户; 2:自定义用户
    "displayUserSerial": "",  # 自定义用户关联序列号
    "endTime": 0,  # 结束时间
    "finishJumpEditTemp": "",  # 答题结束跳转前端回显值
    "finishJumpLinkType": 0,  # 答题结束跳转关联类型：1.关联商品列表; 2.关联商品详情页; 3.关联活动; 4.商城内部链接; 5.外部链接;  7.抽奖活动; 9.随心购活动列表; 10.随心购活动详情; 13.魔法专区; 15.S+S+S活动; 16.签约购4.0落地页;'
    "finishJumpPictMobile": "",  # 答题结束跳转链接图片(移动端)
    "finishJumpPictPc": "",  # 答题结束跳转链接图片(PC)
    "finishJumpTargetValue": "",  # 答题结束跳转关联值
    "ipLimit": 0,  # IP答题限制 0.否 1.是
    "ipRefillLimit": 0,  # 每个IP的答题限制次数
    "isDraft": 0,  # 是否保存为草稿 0:否 1:是
    "isEditable": 0,  # 是否允许用户修改上次提交的答案 0:否;1:是;
    "isNotShareable": 0,  # 禁止分享 0:否;1:是;
    "isSetTime": 0,  # 设置问卷起始时间 0.否 1.是
    "isSettle": 0,  # 是否在入口固定: 0.否 1.是
    "isShowStatistics": 0,  # 展示统计结果 0:否;1:是;
    "jumpLinkProductList": [{"serialNo": "", "sort": 0}],  # 答题结束跳转关联产品编码列表
    "jumpLinkPromotion": {
        "activityType": 0,
        "content": "",
        "detailImg": "",
        "isSetBg": 0,
        "listImg": "",
        "promotionId": 0,
        "promotionType": 0,
        "promotionTypeExt": 0,
    },  # 答题结束跳转关联活动信息
    "linkEduCourseId": 0,  # 关联学堂课程的id
    "logics": [
        {"logicType": 0, "questionKey": "", "relateType": 0, "skipCount": 0, "targetQuestionKey": "", "value": ""}
    ],  # 问卷题目逻辑关系
    "memberCustom": {
        "cardEndDate": "",
        "cardStartDate": "",
        "cardStatuses": "",
        "companyCodeList": [{"companyCode": "", "companyName": ""}],
        "limitCardDate": 0,
        "limitLoginDate": 0,
        "limitMemberLevel": 0,
        "limitOrderDate": 0,
        "limitRegDate": 0,
        "loginEndDate": "",
        "loginPlatforms": "",
        "loginStartDate": "",
        "memberLevels": "",
        "memberMaxLevelEndMonth": "",
        "memberMaxLevelStartMonth": "",
        "memberTypes": "",
        "orderEndDate": "",
        "orderStartDate": "",
        "regEndDate": "",
        "regStartDate": "",
    },  # 标签会员信息
    "productCodeList": [],  # 商品编码列表
    "projectDesc": "",  # 问卷项目描述
    "questionnaireChannel": 0,  # 问卷渠道: 1:商城用户 2:外部用户
    "questions": [
        {
            "formData": {},
            "imgUrl": "",
            "inputCheckType": 0,
            "linkUrl": "",
            "options": [
                {
                    "imgUrl": "",
                    "label": "",
                    "labelDesc": "",
                    "linkUrl": "",
                    "other": False,
                    "tags": [{"text": ""}],
                    "value": "",
                }
            ],
            "questionKey": "",
            "selectLimit": 0,
            "subQuestions": [{"questionKey": "", "title": ""}],
            "title": "",
            "type": 0,
        }
    ],  # 问题
    "shareImg": "",  # 问卷分享封面图
    "startTime": 0,  # 开始时间
    "themeImg": "",  # 主题图片(PC)
    "themeImgOfMobile": "",  # 主题图片(移动端)
    "title": "",  # 问卷标题
    "userLimit": 0,  # 商城用户答题限制 0.否 1.是
    "userRefillLimit": 0,  # 商城用户的答题限制次数
    "wechatLimit": 0,  # 微信答题限制 0.否 1.是
    "wechatRefillLimit": 0,  # 每个微信的答题限制次数
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_questionnaire_saveQuestionnaire(data=data, headers=headers):
    """
    添加问卷
    /mgmt/cms/questionnaire/saveQuestionnaire

    参数说明:
    - activityId: 抽奖活动id
    - concluding: 结束语
    - deviceLimit: 设备答题限制 0.否 1.是
    - deviceRefillLimit: 每个设备的答题限制次数
    - displayType: 发布对象类型: 0:所有用户 1:标签用户; 2:自定义用户
    - displayUserSerial: 自定义用户关联序列号
    - endTime: 结束时间
    - finishJumpEditTemp: 答题结束跳转前端回显值
    - finishJumpLinkType: 答题结束跳转关联类型：1.关联商品列表; 2.关联商品详情页; 3.关联活动; 4.商城内部链接; 5.外部链接;  7.抽奖活动; 9.随心购活动列表; 10.随心购活动详情; 13.魔法专区; 15.S+S+S活动; 16.签约购4.0落地页;'
    - finishJumpPictMobile: 答题结束跳转链接图片(移动端)
    - finishJumpPictPc: 答题结束跳转链接图片(PC)
    - finishJumpTargetValue: 答题结束跳转关联值
    - ipLimit: IP答题限制 0.否 1.是
    - ipRefillLimit: 每个IP的答题限制次数
    - isDraft: 是否保存为草稿 0:否 1:是
    - isEditable: 是否允许用户修改上次提交的答案 0:否;1:是;
    - isNotShareable: 禁止分享 0:否;1:是;
    - isSetTime: 设置问卷起始时间 0.否 1.是
    - isSettle: 是否在入口固定: 0.否 1.是
    - isShowStatistics: 展示统计结果 0:否;1:是;
    - jumpLinkProductList: 答题结束跳转关联产品编码列表
    - jumpLinkProductList.serialNo: 产品编码
    - jumpLinkProductList.sort: sort
    - jumpLinkPromotion: 答题结束跳转关联活动信息
    - jumpLinkPromotion.activityType: 活动类型:1-抢购(秒杀),2-换购,4-预售
    - jumpLinkPromotion.content: 活动列表内容
    - jumpLinkPromotion.detailImg: 活动详情背景图
    - jumpLinkPromotion.isSetBg: 是否设置背景图，0：否；1:是
    - jumpLinkPromotion.listImg: 活动列表背景图
    - jumpLinkPromotion.promotionId: 活动ID
    - jumpLinkPromotion.promotionType: 活动类型(活动专区): 1.通用 2:随心购
    - jumpLinkPromotion.promotionTypeExt: 基于抢购活动(activityType=1)类型区分：0-原抢购(秒杀) 1-常规
    - linkEduCourseId: 关联学堂课程的id
    - logics: 问卷题目逻辑关系
    - logics.logicType: 逻辑类型 1.跳转 2.显示
    - logics.questionKey: 问题key
    - logics.relateType: 关联类型: 1.题目 2.选项
    - logics.skipCount: 是否不算入统计: 1.不算入统计 0.算入统计
    - logics.targetQuestionKey: 目标问题key
    - logics.value: 值
    - memberCustom: 标签会员信息
    - memberCustom.cardEndDate: 办卡月份止(yyyy-MM)
    - memberCustom.cardStartDate: 办卡月份起(yyyy-MM)
    - memberCustom.cardStatuses: 会员卡状态 -3:未开卡; -2:未升级; -1:待激活; 0:有效; 1:已失效; 2:已注销(多选使用逗号分隔)
    - memberCustom.companyCodeList: 分公司编号列表
    - memberCustom.companyCodeList.companyCode: 分公司编号
    - memberCustom.companyCodeList.companyName: 分公司名称
    - memberCustom.limitCardDate: 是否限制办卡月份: 0:不限制 1:限制 2:仅当月新开卡
    - memberCustom.limitLoginDate: 是否限制最近访问时间: 0:不限制 1:限制
    - memberCustom.limitMemberLevel: 是否限制顾客等级: 0:不限制 1:限制
    - memberCustom.limitOrderDate: 是否限制最近购货月份: 0:不限制 1:限制 2:从未购货
    - memberCustom.limitRegDate: 是否限制注册月份: 0:不限制 1:限制
    - memberCustom.loginEndDate: 访问时间止(yyyy-MM)
    - memberCustom.loginPlatforms: 登录渠道:1:PC 2:APP 3:小程序
    - memberCustom.loginStartDate: 访问时间起(yyyy-MM)
    - memberCustom.memberLevels: 顾客等级:0.新用户,1.一星优惠客户,2.二星优惠客户,3.三星优惠客户,4.四星优惠客户,5.客户代表,6.客户经理,7.中级客户经理,8.客户总监,9.高级客户总监,10.资深客户总监,11.客户总经理(多选使用逗号分隔)
    - memberCustom.memberMaxLevelEndMonth: 顾客最高等级取值结束月份
    - memberCustom.memberMaxLevelStartMonth: 顾客最高等级取值开始月份
    - memberCustom.memberTypes: 按顾客身份查看 1:会员; 2:vip会员; 3:云商; 4:微店;(多选使用逗号分隔)
    - memberCustom.orderEndDate: 购货月份止(yyyy-MM)
    - memberCustom.orderStartDate: 购货月份起(yyyy-MM)
    - memberCustom.regEndDate: 注册月份止(yyyy-MM)
    - memberCustom.regStartDate: 注册月份起(yyyy-MM)
    - productCodeList: 商品编码列表
    - projectDesc: 问卷项目描述
    - questionnaireChannel: 问卷渠道: 1:商城用户 2:外部用户
    - questions: 问题
    - questions.formData: 表格
    - questions.imgUrl: 图片地址
    - questions.inputCheckType: 属性验证:0.不验证1.手机号2.身份证号3.省市区
    - questions.linkUrl: 关联链接
    - questions.options: 选项
    - questions.options.imgUrl: 图片
    - questions.options.label: 选项
    - questions.options.labelDesc: 选项说明
    - questions.options.linkUrl: 超链接
    - questions.options.tags: 选项标签
    - questions.options.tags.text: 标签值
    - questions.options.value: 值
    - questions.questionKey: 问题key
    - questions.selectLimit: 多选题最多可选数量控制
    - questions.subQuestions: 子问题
    - questions.subQuestions.questionKey: 问题key
    - questions.subQuestions.title: 问题标题
    - questions.title: 选项标题
    - questions.type: 表单项类型 1:填空; 2:单选; 3:多选; 4:评分; 5:评价; 6:比重; 7:排序; 8:多项填空题 9:表格数值题 10.上传文件题
    - shareImg: 问卷分享封面图
    - startTime: 开始时间
    - themeImg: 主题图片(PC)
    - themeImgOfMobile: 主题图片(移动端)
    - title: 问卷标题
    - userLimit: 商城用户答题限制 0.否 1.是
    - userRefillLimit: 商城用户的答题限制次数
    - wechatLimit: 微信答题限制 0.否 1.是
    - wechatRefillLimit: 每个微信的答题限制次数
    """

    url = "/mgmt/cms/questionnaire/saveQuestionnaire"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

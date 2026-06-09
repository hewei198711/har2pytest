"""
濞村鐦� swagger_updater.py 濡€虫健
"""

import asyncio

import allure

from har2pytest.config import APIConfig
from har2pytest.swagger_handler import SwaggerHandler


@allure.feature("Swagger閺傚洦銆傞弴瀛樻煀閸ｏ拷")

@allure.story("绾喖鐣鹃張宥呭閸栵拷")

def test_determine_service_package():

    """濞村鐦弽瑙勫祦URL閸掋倖鏌囬張宥呭閸栵拷"""

    # 鐟欙箑褰傞柊宥囩枂閸掓繂顫愰崠锟�

    APIConfig.get_config("SERVICE_MAPPING")



    # 娑撳瓨妞傜拋鍓х枂 SERVICE_MAPPING 闁板秶鐤�

    original_service_mapping = APIConfig._config.get("SERVICE_MAPPING", {})

    APIConfig._config["SERVICE_MAPPING"] = {"mobile": "mall_mobile_application", "user": "mall_center_user"}



    try:

        assert APIConfig.determine_service_package("/mobile/trade/orderCommit") == "mall_mobile_application"

        assert APIConfig.determine_service_package("/user/123/info") == "mall_center_user"

        assert APIConfig.determine_service_package("") == "apis"

    finally:

        # 閹垹顦查崢鐔奉潗闁板秶鐤�

        APIConfig._config["SERVICE_MAPPING"] = original_service_mapping





@allure.feature("Swagger閺傚洦銆傞弴瀛樻煀閸ｏ拷")

@allure.story("閸︹娍wagger娑擃厽鐓￠幍缍歅I娣団剝浼�")

def test_find_api_info_in_swagger():

    """濞村鐦崷鈯縲agger閺傚洦銆傛稉顓熺叀閹电稓PI娣団剝浼�"""

    updater = SwaggerHandler()



    # 濞村鐦疭wagger閺佺増宓�

    swagger_data = {

        "paths": {

            "/user/login": {

                "post": {

                    "summary": "閻€劍鍩涢惂璇茬秿",

                    "description": "閻€劍鍩涢惂璇茬秿閹恒儱褰�",

                    "parameters": [

                        {"name": "username", "description": "閻€劍鍩涢崥锟�"},

                        {"name": "password", "description": "鐎靛棛鐖�"},

                    ],

                }

            }

        }

    }



    # 濞村鐦弻銉﹀鐎涙ê婀惃鍑橮I

    api_info = updater.find_api_info_in_swagger(swagger_data, "/user/login", "POST")

    assert api_info["summary"] == "閻€劍鍩涢惂璇茬秿"

    assert api_info["description"] == "閻€劍鍩涢惂璇茬秿閹恒儱褰�"

    assert api_info["parameters"]["username"] == "閻€劍鍩涢崥锟�"

    assert api_info["parameters"]["password"] == "鐎靛棛鐖�"



    # 濞村鐦弻銉﹀娑撳秴鐡ㄩ崷銊ф畱API

    api_info = updater.find_api_info_in_swagger(swagger_data, "/nonexistent", "GET")

    assert api_info["summary"] == ""

    assert api_info["description"] == ""

    assert api_info["parameters"] == {}





@allure.feature("Swagger閺傚洦銆傞弴瀛樻煀閸ｏ拷")

@allure.story("鐢泩asePath閻ㄥ嚈PI鐠侯垰绶為崠褰掑帳")

def test_find_api_info_with_basepath():

    """濞村鐦敮顩坅sePath閻ㄥ嚈PI鐠侯垰绶為崠褰掑帳"""

    updater = SwaggerHandler()



    # 濞村鐦敮顩坅sePath閻ㄥ嚪wagger閺佺増宓�

    swagger_data = {

        "basePath": "/appStore",

        "paths": {

            "/storage/upload": {

                "post": {

                    "summary": "閺傚洣娆㈡稉濠佺炊",

                    "description": "閺傚洣娆㈡稉濠佺炊閹恒儱褰�",

                    "parameters": [

                        {"name": "storageType", "description": "鐎涙ê鍋嶇猾璇茬€�"},

                        {"name": "clientKey", "description": "鐎广垺鍩涚粩顖氱槕闁斤拷"},

                    ],

                }

            }

        },

    }



    # 濞村鐦敮顩坅sePath閻ㄥ嚈PI鐠侯垰绶�

    api_info = updater.find_api_info_in_swagger(swagger_data, "/appStore/storage/upload", "POST")

    assert api_info["summary"] == "閺傚洣娆㈡稉濠佺炊"

    assert api_info["description"] == "閺傚洣娆㈡稉濠佺炊閹恒儱褰�"

    assert api_info["parameters"]["storageType"] == "鐎涙ê鍋嶇猾璇茬€�"

    assert api_info["parameters"]["clientKey"] == "鐎广垺鍩涚粩顖氱槕闁斤拷"





@allure.feature("Swagger閺傚洦銆傞弴瀛樻煀閸ｏ拷")

@allure.story("濡€崇€峰鏇犳暏婢跺嫮鎮�")

def test_model_reference_handling():

    """濞村鐦Ο鈥崇€峰鏇犳暏婢跺嫮鎮�"""

    updater = SwaggerHandler()



    # 濞村鐦敮锔侥侀崹瀣穿閻€劎娈慡wagger閺佺増宓�

    swagger_data = {

        "paths": {

            "/user/login": {

                "post": {

                    "summary": "閻€劍鍩涢惂璇茬秿",

                    "description": "閻€劍鍩涢惂璇茬秿閹恒儱褰�",

                    "parameters": [{"name": "dto", "in": "body", "schema": {"$ref": "#/definitions/LoginRequest"}}],

                }

            }

        },

        "definitions": {

            "LoginRequest": {

                "type": "object",

                "properties": {

                    "username": {"type": "string", "description": "閻€劍鍩涢崥锟�"},

                    "password": {"type": "string", "description": "鐎靛棛鐖�"},

                },

            }

        },

    }



    # 濞村鐦Ο鈥崇€峰鏇犳暏婢跺嫮鎮�

    api_info = updater.find_api_info_in_swagger(swagger_data, "/user/login", "POST")

    assert api_info["summary"] == "閻€劍鍩涢惂璇茬秿"

    assert api_info["description"] == "閻€劍鍩涢惂璇茬秿閹恒儱褰�"

    assert api_info["parameters"]["username"] == "閻€劍鍩涢崥锟�"

    assert api_info["parameters"]["password"] == "鐎靛棛鐖�"





@allure.feature("Swagger閺傚洦銆傞弴瀛樻煀閸ｏ拷")

@allure.story("閼惧嘲褰囨妯款吇閸婏拷")

def test_get_default_value():

    """濞村鐦懢宄板絿閸欏倹鏆熸妯款吇閸婏拷"""

    handler = SwaggerHandler()



    # 濞村鐦稉宥呮倱缁鐎烽惃鍕帛鐠併倕鈧拷

    assert handler._get_default_value("string") == ""

    assert handler._get_default_value("int") == 0

    assert handler._get_default_value("integer") == 0

    assert handler._get_default_value("number") == 0.0

    assert handler._get_default_value("float") == 0.0

    assert handler._get_default_value("boolean") is False

    assert handler._get_default_value("array") == []

    assert handler._get_default_value("object") == {}

    # 閺堫亞鐓＄猾璇茬€锋潻鏂挎礀缁屽搫鐡х粭锔胯

    assert handler._get_default_value("unknown") == ""





@allure.feature("Swagger閺傚洦銆傞弴瀛樻煀閸ｏ拷")

@allure.story("娴犲洞wagger閹绘劕褰囬崣鍌涙殶")

def test_extract_params_from_swagger():

    """濞村鐦禒宥磜agger閺傚洦銆傞幓鎰絿閸欏倹鏆�"""

    handler = SwaggerHandler()



    swagger_data = {

        "definitions": {

            "UserRequest": {

                "type": "object",

                "properties": {

                    "username": {"type": "string", "description": "閻€劍鍩涢崥锟�"},

                    "password": {"type": "string", "description": "鐎靛棛鐖�"},

                },

            }

        }

    }



    parameters = [

        {"name": "query_param", "in": "query", "type": "string", "description": "閺屻儴顕楅崣鍌涙殶"},

        {"name": "path_param", "in": "path", "type": "integer", "description": "鐠侯垰绶為崣鍌涙殶"},

        {"name": "body_param", "in": "body", "schema": {"$ref": "#/definitions/UserRequest"}},

    ]



    query_params, post_data, has_query_param, has_body_param, path_params, param_descriptions = (

        handler._extract_params_from_swagger(parameters, swagger_data)

    )



    assert query_params == {"query_param": ""}

    assert path_params == {"path_param": 0}

    assert has_query_param is True

    assert has_body_param is True

    assert param_descriptions["query_param"] == "閺屻儴顕楅崣鍌涙殶"

    assert param_descriptions["path_param"] == "鐠侯垰绶為崣鍌涙殶"

    assert param_descriptions["username"] == "閻€劍鍩涢崥锟�"

    assert param_descriptions["password"] == "鐎靛棛鐖�"





@allure.feature("Swagger閺傚洦銆傞弴瀛樻煀閸ｏ拷")

@allure.story("娴犲洞wagger閹绘劕褰囬崣鍌涙殶-閻╁瓨甯磒roperties")

def test_extract_params_from_swagger_with_properties():

    """濞村鐦禒宥磜agger閺傚洦銆傞幓鎰絿閸欏倹鏆熼敍鍫㈡纯閹侯櫠roperties閿涳拷"""

    handler = SwaggerHandler()



    swagger_data = {}



    parameters = [

        {

            "name": "body",

            "in": "body",

            "schema": {

                "type": "object",

                "properties": {

                    "name": {"type": "string", "description": "閸氬秶袨"},

                    "age": {"type": "integer", "description": "楠炴挳绶�"},

                },

            },

        }

    ]



    query_params, post_data, has_query_param, has_body_param, path_params, param_descriptions = (

        handler._extract_params_from_swagger(parameters, swagger_data)

    )



    assert has_body_param is True

    assert param_descriptions["name"] == "閸氬秶袨"

    assert param_descriptions["age"] == "楠炴挳绶�"





@allure.feature("Swagger閺傚洦銆傞弴瀛樻煀閸ｏ拷")

@allure.story("娴犲洞wagger閹绘劕褰囬崣鍌涙殶-閺冪姴寮弫锟�")

def test_extract_params_from_swagger_empty():

    """濞村鐦禒宥磜agger閺傚洦銆傞幓鎰絿缁屽搫寮弫锟�"""

    handler = SwaggerHandler()



    swagger_data = {}

    parameters = []



    query_params, post_data, has_query_param, has_body_param, path_params, param_descriptions = (

        handler._extract_params_from_swagger(parameters, swagger_data)

    )



    assert query_params == {}

    assert post_data == {}

    assert path_params == {}

    assert has_query_param is False

    assert has_body_param is False

    assert param_descriptions == {}





@allure.feature("Swagger閺傚洦銆傞弴瀛樻煀閸ｏ拷")

@allure.story("Swagger缂傛挸鐡�")

def test_swagger_cache():

    """濞村鐦疭wagger閺傚洦銆傜紓鎾崇摠閺堝搫鍩�"""

    handler = SwaggerHandler()



    test_data = {"paths": {"/test": {"get": {"summary": "test"}}}}

    handler.swagger_cache["http://test.com"] = test_data



    cached_data = handler.swagger_cache.get("http://test.com")

    assert cached_data == test_data

    assert cached_data is not None





@allure.feature("Swagger閺傚洦銆傞弴瀛樻煀閸ｏ拷")

@allure.story("閹绘劕褰嘊ody閸欏倹鏆�-濡€崇€峰鏇犳暏")

def test_extract_body_params_with_ref():

    """濞村鐦禒宥磜agger閺傚洦銆傞幓鎰絿Body閸欏倹鏆熼敍鍫濈敨濡€崇€峰鏇犳暏閿涳拷"""

    handler = SwaggerHandler()



    swagger_data = {

        "definitions": {

            "LoginRequest": {

                "type": "object",

                "properties": {

                    "username": {"type": "string", "description": "閻€劍鍩涢崥锟�"},

                    "password": {"type": "string", "description": "鐎靛棛鐖�"},

                },

            }

        }

    }



    schema = {"$ref": "#/definitions/LoginRequest"}

    body_params = handler._extract_body_params(schema, swagger_data)



    assert body_params == {"username": "", "password": ""}





@allure.feature("Swagger閺傚洦銆傞弴瀛樻煀閸ｏ拷")

@allure.story("閹绘劕褰嘊ody閸欏倹鏆�-閻╁瓨甯寸仦鐐粹偓锟�")

def test_extract_body_params_with_properties():

    """濞村鐦禒宥磜agger閺傚洦銆傞幓鎰絿Body閸欏倹鏆熼敍鍫㈡纯閹侯櫠roperties閿涳拷"""

    handler = SwaggerHandler()



    swagger_data = {}



    schema = {

        "type": "object",

        "properties": {

            "name": {"type": "string"},

            "age": {"type": "integer"},

        },

    }

    body_params = handler._extract_body_params(schema, swagger_data)



    assert body_params == {"name": "", "age": 0}





@allure.feature("Swagger閺傚洦銆傞弴瀛樻煀閸ｏ拷")

@allure.story("閹绘劕褰嘊ody閸欏倹鏆�-缁岀皧chema")

def test_extract_body_params_empty_schema():

    """濞村鐦禒宥磜agger閺傚洦銆傞幓鎰絿Body閸欏倹鏆熼敍鍫⑩敄schema閿涳拷"""

    handler = SwaggerHandler()



    swagger_data = {}

    schema = {}

    body_params = handler._extract_body_params(schema, swagger_data)



    assert body_params == {}





@allure.feature("Swagger閺傚洦銆傞弴瀛樻煀閸ｏ拷")

@allure.story("閹绘劕褰嘊ody閸欏倹鏆�-瀵洜鏁ゆ稉宥呯摠閸︼拷")

def test_extract_body_params_ref_not_found():

    """濞村鐦禒宥磜agger閺傚洦銆傞幓鎰絿Body閸欏倹鏆熼敍鍫濈穿閻€劋绗夌€涙ê婀敍锟�"""

    handler = SwaggerHandler()



    swagger_data = {"definitions": {}}



    schema = {"$ref": "#/definitions/NonExistent"}

    body_params = handler._extract_body_params(schema, swagger_data)



    assert body_params == {}





@allure.feature("Swagger閺傚洦銆傞弴瀛樻煀閸ｏ拷")

@allure.story("閺屻儲澹楢PI娣団剝浼�-鐠侯垰绶炴稉宥呯摠閸︼拷")

def test_find_api_info_path_not_found():

    """濞村鐦崷鈯縲agger閺傚洦銆傛稉顓熺叀閹靛彞绗夌€涙ê婀惃鍕熅瀵帮拷"""

    updater = SwaggerHandler()



    swagger_data = {"paths": {"/user/login": {"post": {"summary": "閻ц缍�"}}}}



    api_info = updater.find_api_info_in_swagger(swagger_data, "/nonexistent/path", "GET")



    assert api_info["summary"] == ""

    assert api_info["description"] == ""

    assert api_info["parameters"] == {}





@allure.feature("Swagger閺傚洦銆傞弴瀛樻煀閸ｏ拷")

@allure.story("閺屻儲澹楢PI娣団剝浼�-閺傝纭舵稉宥呯摠閸︺劋绲鹃張澶愭缁撅拷")

def test_find_api_info_method_not_found_but_has_fallback():

    """濞村鐦崷鈯縲agger閺傚洦銆傛稉顓熺叀閹垫儳鐡ㄩ崷銊ㄧ熅瀵板嫪绲炬稉宥呯摠閸︺劍鏌熷▔鏇礉娴ｅ棙婀侀梽宥囬獓閺傝纭�"""

    updater = SwaggerHandler()



    swagger_data = {

        "paths": {

            "/user/login": {

                "post": {"summary": "閻ц缍�", "description": "閻€劍鍩涢惂璇茬秿"},

            }

        }

    }



    api_info = updater.find_api_info_in_swagger(swagger_data, "/user/login", "get")



    assert api_info["summary"] == "閻ц缍�"

    assert api_info["description"] == "閻€劍鍩涢惂璇茬秿"





@allure.feature("Swagger閺傚洦銆傞弴瀛樻煀閸ｏ拷")

@allure.story("閺屻儲澹楢PI娣団剝浼�-缁岀癄wagger閺佺増宓�")

def test_find_api_info_empty_swagger_data():

    """濞村鐦崷銊р敄Swagger閺佺増宓佹稉顓熺叀閹电稓PI"""

    updater = SwaggerHandler()



    api_info = updater.find_api_info_in_swagger({}, "/user/login", "POST")

    assert api_info["summary"] == ""

    assert api_info["description"] == ""

    assert api_info["parameters"] == {}





@allure.feature("Swagger閺傚洦銆傞弴瀛樻煀閸ｏ拷")

@allure.story("閺屻儲澹楢PI娣団剝浼�-缁岀皢aths")

def test_find_api_info_empty_paths():

    """濞村鐦崷銊р敄paths娑擃厽鐓￠幍缍歅I"""

    updater = SwaggerHandler()



    swagger_data = {"paths": {}}

    api_info = updater.find_api_info_in_swagger(swagger_data, "/user/login", "POST")



    assert api_info["summary"] == ""

    assert api_info["description"] == ""

    assert api_info["parameters"] == {}





@allure.feature("Swagger閺傚洦銆傞弴瀛樻煀閸ｏ拷")

@allure.story("閺屻儲澹楢PI娣団剝浼�-鐢拷$ref閸欏倹鏆�")

def test_find_api_info_with_param_ref():

    """濞村鐦崷鈯縲agger閺傚洦銆傛稉顓熺叀閹垫儳鐢�$ref瀵洜鏁ら惃鍑橮I閸欏倹鏆�"""

    updater = SwaggerHandler()



    swagger_data = {

        "paths": {

            "/user/create": {

                "post": {

                    "summary": "閸掓稑缂撻悽銊﹀煕",

                    "description": "閸掓稑缂撻弬鎵暏閹达拷",

                    "parameters": [

                        {

                            "name": "user",

                            "in": "body",

                            "schema": {"$ref": "#/definitions/User"},

                        }

                    ],

                }

            }

        },

        "definitions": {

            "User": {

                "type": "object",

                "properties": {

                    "name": {"type": "string", "description": "閻€劍鍩涢崥宥囆�"},

                    "email": {"type": "string", "description": "閻€劍鍩涢柇顔绢唸"},

                },

            }

        },

    }



    api_info = updater.find_api_info_in_swagger(swagger_data, "/user/create", "POST")



    assert api_info["summary"] == "閸掓稑缂撻悽銊﹀煕"

    assert api_info["description"] == "閸掓稑缂撻弬鎵暏閹达拷"

    assert api_info["parameters"]["name"] == "閻€劍鍩涢崥宥囆�"

    assert api_info["parameters"]["email"] == "閻€劍鍩涢柇顔绢唸"





@allure.feature("Swagger閺傚洦銆傞弴瀛樻煀閸ｏ拷")

@allure.story("閺屻儲澹楢PI娣団剝浼�-婢舵氨顫扝TTP閺傝纭堕梽宥囬獓")

def test_find_api_info_method_fallback():

    """濞村鐦崷鈯縲agger閺傚洦銆傛稉顓熺叀閹电稓PI閺冪TTP閺傝纭堕惃鍕缁狙冾槱閻烇拷"""

    updater = SwaggerHandler()



    swagger_data = {

        "paths": {

            "/user/login": {

                "put": {

                    "summary": "閺囧瓨鏌婇惂璇茬秿娣団剝浼�",

                    "description": "閺囧瓨鏌婇惂璇茬秿娣団剝浼�",

                    "parameters": [],

                }

            }

        }

    }



    api_info = updater.find_api_info_in_swagger(swagger_data, "/user/login", "post")



    assert api_info["summary"] == "閺囧瓨鏌婇惂璇茬秿娣団剝浼�"

    assert api_info["description"] == "閺囧瓨鏌婇惂璇茬秿娣団剝浼�"





@allure.feature("Swagger閺傚洦銆傞弴瀛樻煀閸ｏ拷")

@allure.story("閼惧嘲褰囨妯款吇閸婏拷-閺堫亞鐓＄猾璇茬€�")

def test_get_default_value_unknown_type():

    """濞村鐦懢宄板絿閺堫亞鐓￠崣鍌涙殶缁鐎烽惃鍕帛鐠併倕鈧拷"""

    handler = SwaggerHandler()



    assert handler._get_default_value("unknown_type") == ""

    assert handler._get_default_value("date") == ""

    assert handler._get_default_value("file") == ""





@allure.feature("Swagger閺傚洦銆傞弴瀛樻煀閸ｏ拷")

@allure.story("SwaggerHandler閸掓繂顫愰崠锟�")

def test_swagger_handler_init():

    """濞村鐦疭waggerHandler閸掓繂顫愰崠锟�"""

    handler = SwaggerHandler()



    assert handler.swagger_cache == {}

    assert handler.api_generator is None





@allure.feature("Swagger閺傚洦銆傞弴瀛樻煀閸ｏ拷")

@allure.story("Swagger閺傚洦銆傞懢宄板絿-閸ョ偤鈧偓鐠侯垰绶�")

def test_get_swagger_doc_fallback_paths(monkeypatch):

    """濞村鐦ぐ鎼抴agger-resources婢惰精瑙﹂弮璁圭礉閸ョ偤鈧偓閸掓澘鐖剁憴浣界熅瀵帮拷"""

    handler = SwaggerHandler()



    call_count = [0]



    async def mock_send_request(url):

        call_count[0] += 1

        if call_count[0] == 1:

            raise Exception("swagger-resources failed")

        elif call_count[0] == 2:

            return None

        else:

            return {"paths": {"/api/test": {"get": {}}}}



    monkeypatch.setattr(handler, "_send_request", mock_send_request)



    result = asyncio.run(handler.get_swagger_doc("https://example.com"))



    assert result is not None

    assert "paths" in result

    assert "/api/test" in result["paths"]





@allure.feature("Swagger閺傚洦銆傞弴瀛樻煀閸ｏ拷")

@allure.story("Swagger閺傚洦銆傞懢宄板絿-閹碘偓閺堝鐭惧鍕厴婢惰精瑙�")

def test_get_swagger_doc_all_paths_failed(monkeypatch):

    """濞村鐦ぐ鎾村閺堝鐭惧鍕厴婢惰精瑙﹂弮鎯扮箲閸ユ慷one"""

    handler = SwaggerHandler()



    async def mock_send_request(url):

        raise Exception("all paths failed")



    monkeypatch.setattr(handler, "_send_request", mock_send_request)



    result = asyncio.run(handler.get_swagger_doc("https://example.com"))



    assert result is None





@allure.feature("Swagger閺傚洦銆傞弴瀛樻煀閸ｏ拷")

@allure.story("Swagger閺傚洦銆傞懢宄板絿-閺嶇厧绱℃稉宥嗩劀绾拷")

def test_get_swagger_doc_invalid_format(monkeypatch):

    """濞村鐦潻鏂挎礀閻ㄥ嫭鏋冨锝嗙壐瀵繋绗夊锝団€橀敍鍫㈠繁鐏忔唲aths鐎涙顔岄敍锟�"""

    handler = SwaggerHandler()



    call_count = [0]



    async def mock_send_request(url):

        call_count[0] += 1

        if call_count[0] == 1:

            raise Exception("swagger-resources failed")

        elif call_count[0] == 2:

            return {"info": {"title": "Test"}}

        else:

            return {"paths": {"/api/test": {"get": {}}}}



    monkeypatch.setattr(handler, "_send_request", mock_send_request)



    result = asyncio.run(handler.get_swagger_doc("https://example.com"))



    assert result is not None

    assert "paths" in result





@allure.feature("Swagger閺傚洦銆傞弴瀛樻煀閸ｏ拷")

@allure.story("娴犲洞wagger閻㈢喐鍨欰PI閺傚洣娆�")

def test_generate_apis_from_swagger_with_basepath(tmp_path, monkeypatch):

    """濞村鐦禒宥磜agger閺傚洦銆傞悽鐔稿灇API閺傚洣娆㈤敍鍫濈敨basePath閿涳拷"""

    swagger_data = {

        "swagger": "2.0",

        "basePath": "/api/v1",

        "paths": {

            "/users": {

                "get": {

                    "summary": "閼惧嘲褰囬悽銊﹀煕閸掓銆�",

                    "parameters": [

                        {"name": "page", "in": "query", "type": "integer"},

                    ],

                }

            }

        },

    }



    handler = SwaggerHandler()

    async def _mock_get_swagger(url): return swagger_data
    monkeypatch.setattr(handler, "get_swagger_doc", _mock_get_swagger)

    async def mock_gen(self, req, force, info):
        return str(tmp_path / "api_users.py")

    api_generator_mock = type("MockApiGenerator", (), {"generate_api_file": mock_gen})()
    handler.api_generator = api_generator_mock

    result = asyncio.run(handler.generate_apis_from_swagger("https://example.com"))

    assert len(result) == 1
    assert "api_users.py" in result[0]


@allure.feature("Swagger閺傚洦銆傞弴瀛樻煀閸ｏ拷")
@allure.story("娴犲洞wagger閻㈢喐鍨欰PI閺傚洣娆�-閹稿洤鐣鹃悧鐟扮暰鐠侯垰绶�")
def test_generate_apis_from_swagger_specific_path(tmp_path, monkeypatch):
    """濞村鐦禒宥磜agger閺傚洦銆傞悽鐔稿灇閹稿洤鐣剧捄顖氱窞閻ㄥ嚈PI閺傚洣娆�"""
    swagger_data = {
        "swagger": "2.0",
        "paths": {"/users": {"get": {"summary": "閻€劍鍩涢崚妤勩€�"}}, "/products": {"get": {"summary": "娴溠冩惂閸掓銆�"}}},
    }

    handler = SwaggerHandler()

    async def _mock_get_swagger(url): return swagger_data
    monkeypatch.setattr(handler, "get_swagger_doc", _mock_get_swagger)

    async def mock_gen(self, req, force, info):
        return str(tmp_path / "api_users.py")

    api_generator_mock = type("MockApiGenerator", (), {"generate_api_file": mock_gen})()
    handler.api_generator = api_generator_mock

    result = asyncio.run(handler.generate_apis_from_swagger("https://example.com", specific_path="/users"))

    assert len(result) == 1
    assert "api_users.py" in result[0]


@allure.feature("Swagger閺傚洦銆傞弴瀛樻煀閸ｏ拷")
@allure.story("娴犲洞wagger閻㈢喐鍨欰PI閺傚洣娆�-閼惧嘲褰囬弬鍥ㄣ€傛径杈Е")
def test_generate_apis_from_swagger_doc_failed(monkeypatch):
    """濞村鐦ぐ鎾存￥濞夋洝骞忛崣鏈agger閺傚洦銆傞弮鎯扮箲閸ョ偟鈹栭崚妤勩€�"""
    handler = SwaggerHandler()

    async def _mock_get_swagger_none(url): return None
    monkeypatch.setattr(handler, "get_swagger_doc", _mock_get_swagger_none)

    result = asyncio.run(handler.generate_apis_from_swagger("https://example.com"))

    assert result == []





@allure.feature("Swagger閺傚洦銆傞弴瀛樻煀閸ｏ拷")

@allure.story("娴犲洞wagger閻㈢喐鍨欰PI閺傚洣娆�-閸欏倹鏆熼幓鎰絿")

def test_generate_apis_from_swagger_extract_params(tmp_path, monkeypatch):

    """濞村鐦禒宥磜agger閺傚洦銆傞幓鎰絿閸欏倹鏆熼獮鍓佹晸閹存€塒I閺傚洣娆�"""

    swagger_data = {

        "swagger": "2.0",

        "paths": {

            "/users/{userId}": {

                "get": {

                    "summary": "閼惧嘲褰囬悽銊﹀煕鐠囷附鍎�",

                    "parameters": [

                        {"name": "userId", "in": "path", "type": "integer", "description": "閻€劍鍩汭D"},

                        {"name": "includeDetails", "in": "query", "type": "boolean"},

                    ],

                }

            }

        },

    }



    handler = SwaggerHandler()



    async def _mock_get_swagger(url): return swagger_data
    monkeypatch.setattr(handler, "get_swagger_doc", _mock_get_swagger)



    captured_request_info = []

    class MockApiGenerator:
        async def generate_api_file(self, request_info, force_overwrite, swagger_info):
            captured_request_info.append(request_info)
            return str(tmp_path / "api_users_userId.py")

    handler.api_generator = MockApiGenerator()

    result = asyncio.run(handler.generate_apis_from_swagger("https://example.com"))



    assert len(result) == 1

    assert len(captured_request_info) == 1



    request_info = captured_request_info[0]



    assert request_info["path_params"] == {"userId": 0}

    assert request_info["query_params"] == {"includeDetails": False}





@allure.feature("Swagger閺傚洦銆傞弴瀛樻煀閸ｏ拷")

@allure.story("Swagger閺佺増宓侀懢宄板絿-缂傛挸鐡ㄩ張鍝勫煑")

def test_get_swagger_doc_caching(monkeypatch):

    """濞村鐦疭wagger閺傚洦銆傞懢宄板絿閻ㄥ嫮绱︾€涙ɑ婧€閸掞拷"""

    handler = SwaggerHandler()



    swagger_data = {"paths": {"/api/test": {"get": {}}}}



    call_count = [0]



    async def mock_send_request(url):

        call_count[0] += 1

        # 缁楊兛绔村▎陇鐨熼悽鈺痺agger-resources鏉╂柨娲栫粚鐚寸礉閻掕泛鎮楅幋鎰閼惧嘲褰�/v3/api-docs

        if call_count[0] == 1:

            return None  # swagger-resources鏉╂柨娲栫粚锟�

        elif call_count[0] == 2:

            return swagger_data  # /v3/api-docs閹存劕濮�

        return None



    monkeypatch.setattr(handler, "_send_request", mock_send_request)



    # 缁楊兛绔村▎陇鐨熼悽锟� - 鎼存棁顕氱拫鍐暏_send_request娑撱倖顐奸敍鍧皐agger-resources婢惰精瑙﹂敍宀€鍔ч崥锟�/v3/api-docs閹存劕濮涢敍锟�

    result1 = asyncio.run(handler.get_swagger_doc("https://example.com"))



    # 缁楊兛绨╁▎陇鐨熼悽銊ф祲閸氬RL - 鎼存棁顕氭担璺ㄦ暏缂傛挸鐡ㄩ敍灞肩瑝鐠嬪啰鏁send_request

    result2 = asyncio.run(handler.get_swagger_doc("https://example.com"))



    # 妤犲矁鐦夌粭顑跨癌濞喡ょ殶閻€劋濞囬悽銊ょ啊缂傛挸鐡�

    assert call_count[0] == 2  # 缁楊兛绔村▎陇鐨熼悽銊ф畱娑撱倖顐肩拠閿嬬湴

    assert result1 == swagger_data

    assert result2 == swagger_data





@allure.feature("Swagger閺傚洦銆傞弴瀛樻煀閸ｏ拷")

@allure.story("閼惧嘲褰嘢wagger閺傚洦銆�-缂傛挸鐡ㄥù瀣槸")

def test_get_swagger_doc_cache():

    """濞村鐦疭wagger閺傚洦銆傜紓鎾崇摠閺堝搫鍩�"""

    handler = SwaggerHandler()



    test_doc = {"paths": {"/test": {"get": {"summary": "test"}}}}

    handler.swagger_cache["http://cached.com"] = test_doc



    cached_doc = asyncio.run(handler.get_swagger_doc("http://cached.com"))



    assert cached_doc == test_doc





@allure.feature("Swagger閺傚洦銆傞弴瀛樻煀閸ｏ拷")

@allure.story("閹绘劕褰囬崣鍌涙殶-鐢附鐏囨稉鎯р偓锟�")

def test_extract_params_with_enum():

    """濞村鐦禒宥磜agger閺傚洦銆傞幓鎰絿鐢附鐏囨稉鎯р偓鑲╂畱閸欏倹鏆�"""

    handler = SwaggerHandler()



    swagger_data = {}

    parameters = [

        {

            "name": "status",

            "in": "query",

            "type": "string",

            "description": "閻樿埖鈧拷",

            "enum": ["active", "inactive"],

        }

    ]



    query_params, post_data, has_query_param, has_body_param, path_params, param_descriptions = (

        handler._extract_params_from_swagger(parameters, swagger_data)

    )



    assert query_params == {"status": ""}

    assert has_query_param is True

    assert param_descriptions["status"] == "閻樿埖鈧拷"





@allure.feature("Swagger閺傚洦銆傞弴瀛樻煀閸ｏ拷")

@allure.story("閹绘劕褰囬崣鍌涙殶-鐠侯垰绶為崣鍌涙殶婢跺嫮鎮�")

def test_extract_params_path_param():

    """濞村鐦禒宥磜agger閺傚洦銆傞幓鎰絿鐠侯垰绶為崣鍌涙殶"""

    handler = SwaggerHandler()



    swagger_data = {}

    parameters = [

        {

            "name": "userId",

            "in": "path",

            "type": "integer",

            "description": "閻€劍鍩汭D",

            "required": True,

        }

    ]



    query_params, post_data, has_query_param, has_body_param, path_params, param_descriptions = (

        handler._extract_params_from_swagger(parameters, swagger_data)

    )



    assert path_params == {"userId": 0}

    assert param_descriptions["userId"] == "閻€劍鍩汭D"





@allure.feature("Swagger閺傚洦銆傞弴瀛樻煀閸ｏ拷")

@allure.story("閹绘劕褰囬崣鍌涙殶-body閸欏倹鏆熼惄瀛樺复properties")

def test_extract_params_body_with_properties():

    """濞村鐦禒宥磜agger閺傚洦銆傞幓鎰絿body閸欏倹鏆熼敍鍫㈡纯閹侯櫠roperties閿涳拷"""

    handler = SwaggerHandler()



    swagger_data = {}

    parameters = [

        {

            "name": "body",

            "in": "body",

            "schema": {

                "type": "object",

                "properties": {

                    "id": {"type": "integer", "description": "ID"},

                    "name": {"type": "string", "description": "閸氬秶袨"},

                },

            },

        }

    ]



    query_params, post_data, has_query_param, has_body_param, path_params, param_descriptions = (

        handler._extract_params_from_swagger(parameters, swagger_data)

    )



    assert post_data == {"id": 0, "name": ""}

    assert has_body_param is True

    assert param_descriptions["id"] == "ID"

    assert param_descriptions["name"] == "閸氬秶袨"



@allure.feature("Swagger閿熺禍ch閿熺禎閿熺禍hV")

@allure.story("閿熺禋閿熺祳閿熺祳pe<P-$ref_(u閿熺祾IN")

def test_extract_param_value_with_ref():

    """Km璜巁extract_param_value閿熺禍閿熺担Yt$ref_(u"""

    handler = SwaggerHandler()



    swagger_data = {

        "definitions": {

            "User": {

                "properties": {

                    "id": {"type": "integer"},

                    "name": {"type": "string"},

                }

            }

        }

    }



    prop_info = {"$ref": "#/definitions/User"}

    result = handler._extract_param_value(prop_info, swagger_data)



    assert result == {"id": 0, "name": ""}






@allure.feature("Swagger閿熺禍ch閿熺禎閿熺禍hV")

@allure.story("閿熺禋閿熺祳閿熺祳pe<P-L]WY閿熺祾a閿熺党|閿熺祹")

def test_extract_param_value_nested_object():

    """Km璜巁extract_param_value閿熺禍閿熺担YtL]WY閿熺祾a閿燂拷"""

    handler = SwaggerHandler()



    swagger_data = {}

    prop_info = {

        "type": "object",

        "properties": {

            "address": {

                "type": "object",

                "properties": {

                    "city": {"type": "string"},

                    "street": {"type": "string"},

                }

            },

            "name": {"type": "string"},

        }

    }



    result = handler._extract_param_value(prop_info, swagger_data)



    assert result == {"address": {"city": "", "street": ""}, "name": ""}






@allure.feature("Swagger閿熺禍ch閿熺禎閿熺禍hV")

@allure.story("閿熺禋閿熺祳閿熺祳pe<P-zz閿熺祾a閿燂拷")

def test_extract_param_value_empty_object():

    """Km璜巁extract_param_value閿熺禍閿熺担Ytzz閿熺祾a閿燂拷"""

    handler = SwaggerHandler()



    swagger_data = {}

    prop_info = {"type": "object"}



    result = handler._extract_param_value(prop_info, swagger_data)



    assert result == {}






@allure.feature("Swagger閿熺禍ch閿熺禎閿熺禍hV")

@allure.story("閿熺禋閿熺祳閿熺祳pe<P-pe閿熺刀{|閿熺祹&^$ref")

def test_extract_param_value_array_with_ref():

    """Km璜巁extract_param_value閿熺禍閿熺担Yt&^$ref閿熺淡pe閿熺刀"""

    handler = SwaggerHandler()



    swagger_data = {

        "definitions": {

            "Item": {

                "properties": {

                    "id": {"type": "integer"},

                    "name": {"type": "string"},

                }

            }

        }

    }



    prop_info = {

        "type": "array",

        "items": {"$ref": "#/definitions/Item"}

    }



    result = handler._extract_param_value(prop_info, swagger_data)



    assert result == [{"id": 0, "name": ""}]






@allure.feature("Swagger閿熺禍ch閿熺禎閿熺禍hV")

@allure.story("閿熺禋閿熺祳閿熺祳pe<P-pe閿熺刀{|閿熺祹&^properties")

def test_extract_param_value_array_with_properties():

    """Km璜巁extract_param_value閿熺禍閿熺担Yt&^properties閿熺淡pe閿熺刀"""

    handler = SwaggerHandler()



    swagger_data = {}

    prop_info = {

        "type": "array",

        "items": {

            "type": "object",

            "properties": {

                "id": {"type": "integer"},

                "name": {"type": "string"},

            }

        }

    }



    result = handler._extract_param_value(prop_info, swagger_data)



    assert result == [{"id": 0, "name": ""}]






@allure.feature("Swagger閿熺禍ch閿熺禎閿熺禍hV")

@allure.story("閿熺禋閿熺祳閿熺祳pe<P-zzpe閿熺刀")


@allure.feature("Swagger閺傚洦銆傞弴瀛樻煀閸ｏ拷")
@allure.story("閹绘劕褰囬崣鍌涙殶閸婏拷-缁岀儤鏆熺紒锟�")
def test_extract_param_value_empty_array():
    """濞村鐦痏extract_param_value閺傝纭舵径鍕倞缁岀儤鏆熺紒锟�"""
    handler = SwaggerHandler()

    swagger_data = {}
    prop_info = {"type": "array"}

    result = handler._extract_param_value(prop_info, swagger_data)

    assert result == []

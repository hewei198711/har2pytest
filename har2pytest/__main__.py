# coding:utf-8
"""
har2pytest 命令行入口
"""

from .config import APIConfig
from .har_parser import HARParser
from .api_generator import APIGenerator
from .testcase_generator import TestCaseGenerator
from .swagger_updater import SwaggerDocUpdater
from .logger import logger


def main():
    """
    主函数 - 支持多种命令行操作模式

    支持的命令：
    1. generate - 从HAR文件生成API接口文件
    2. update - 更新现有API文件的文档信息
    3. summary - 显示HAR文件的API请求摘要
    4. help - 显示帮助信息

    示例用法:
        # 从HAR文件生成API文件
        har2pytest generate api_request.har api

        # 使用默认参数生成
        har2pytest

        # 更新API文档信息
        har2pytest update api

        # 查看HAR文件摘要
        har2pytest summary api_request.har

        # 显示帮助
        har2pytest help
        har2pytest --help
    """
    import sys

    # 初始化配置
    APIConfig._load_config()

    if len(sys.argv) > 1:
        command = sys.argv[1]
        # 处理 --help 选项
        if command == "--help":
            command = "help"
    else:
        command = "generate"

    if command == "generate":
        har_file = "api_request.har"
        output_dir = APIConfig.DEFAULT_SERVICE_PACKAGE()
        force_overwrite = False  # 默认不覆盖

        # 解析参数：har2pytest generate [har_file] [output_dir] [--overwrite]
        args = sys.argv[2:]
        
        for arg in args:
            if arg in ["--overwrite", "-f"]:
                force_overwrite = True
            elif not har_file or har_file == "api_request.har":
                # 简单的位置参数解析逻辑：第一个非flag参数作为 har_file
                # 注意：这里为了兼容旧用法，如果用户只传了 har_file，它会覆盖默认值
                if arg.endswith(".har"):
                    har_file = arg
                else:
                    # 如果第二个参数不是 .har 结尾，可能是 output_dir
                    output_dir = arg
            
        # 更稳健的解析方式（推荐替换上面的简单循环，如果参数顺序固定）：
        # 假设用法: har2pytest generate <har_file> <output_dir> --overwrite
        positional_args = [arg for arg in args if arg not in ["--overwrite", "-f"]]
        if len(positional_args) >= 1:
            har_file = positional_args[0]
        if len(positional_args) >= 2:
            output_dir = positional_args[1]

        logger.info(f"从HAR文件生成API接口文件: {har_file}")
        logger.info(f"输出目录: {output_dir}")
        logger.info(f"强制覆盖: {force_overwrite}") # 新增日志
        logger.info("-" * 50)

        generator = APIGenerator(output_dir)
        generated_files = generator.generate_api_files_from_har(har_file, force_overwrite=force_overwrite)

        logger.info("-" * 50)
        logger.info(f"共生成 {len(generated_files)} 个API接口文件")

        if generated_files:
            generator.generate_index_file(generated_files)

    elif command == "testcase":
        har_file = "api_request.har"
        output_dir = APIConfig.TESTCASE_DIR()
        sub_command = None
        task_id = None
        target_url = None

        if len(sys.argv) > 2:
            sub_command = sys.argv[2]

        if sub_command == "list_query":
            if len(sys.argv) > 3:
                task_id = sys.argv[3]
            if len(sys.argv) > 4:
                har_file = sys.argv[4]

            logger.info(f"生成查询类测试用例: {har_file}")
            logger.info(f"任务ID: {task_id}")
            logger.info("-" * 50)

            generator = TestCaseGenerator(api_dir="api", output_dir="testcases")
            test_files = generator.generate_list_query_testcases(har_file, task_id)

            logger.info("-" * 50)
            if test_files:
                logger.info(f"成功生成 {len(test_files)} 个测试用例文件:")
                for test_file in test_files:
                    logger.info(f"  - {test_file}")
            else:
                logger.info("生成测试用例文件失败")

        elif sub_command == "complex_scenario":
            if len(sys.argv) > 3:
                task_id = sys.argv[3]
            if len(sys.argv) > 4:
                target_url = sys.argv[4]
            if len(sys.argv) > 5:
                har_file = sys.argv[5]

            if target_url and target_url.endswith(".har"):
                har_file = target_url
                target_url = None

            if task_id and task_id.startswith("test_"):
                task_id = task_id[5:]

            logger.info(f"生成复杂场景测试用例: {har_file}")
            logger.info(f"任务ID: {task_id}")
            logger.info(f"目标接口: {target_url or '(自动选择第一个)'}")
            logger.info("-" * 50)

            generator = TestCaseGenerator(api_dir="api", output_dir="testcases")
            test_file = generator.generate_complex_scenario_testcase(har_file, target_url, task_id)

            logger.info("-" * 50)
            if test_file:
                logger.info(f"成功生成测试用例文件: {test_file.replace('\\', '/')}")
            else:
                logger.info("生成测试用例文件失败")

        else:
            if len(sys.argv) > 2:
                har_file = sys.argv[2]
            if len(sys.argv) > 3:
                output_dir = sys.argv[3]

            logger.info(f"从HAR文件生成pytest用例: {har_file}")
            logger.info(f"输出目录: {output_dir}")
            logger.info("-" * 50)

            generator = TestCaseGenerator(api_dir="api", output_dir=output_dir)
            test_file = generator.generate_test_case_from_har(har_file)

            logger.info("-" * 50)
            if test_file:
                logger.info(f"成功生成测试用例文件: {test_file.replace('\\', '/')}")
            else:
                logger.info("生成测试用例文件失败")

    elif command == "update":
        api_dir = APIConfig.DEFAULT_SERVICE_PACKAGE()
        if len(sys.argv) > 2:
            api_dir = sys.argv[2]

        logger.info(f"更新API目录中的文档信息: {api_dir}")
        logger.info("-" * 50)

        updater = SwaggerDocUpdater()
        updater.scan_and_update_apis(api_dir)

    elif command == "swagger":
        swagger_url = None
        output_dir = APIConfig.DEFAULT_SERVICE_PACKAGE()
        force_overwrite = False

        # 解析参数：har2pytest swagger <swagger_url> [output_dir] [--overwrite]
        args = sys.argv[2:]

        for arg in args:
            if arg in ["--overwrite", "-f"]:
                force_overwrite = True
            elif not swagger_url:
                swagger_url = arg
            else:
                output_dir = arg

        if not swagger_url:
            logger.error("错误: 必须提供Swagger文档URL")
            logger.info("使用 'har2pytest help' 查看帮助信息")
            return

        logger.info(f"从Swagger文档生成API接口文件: {swagger_url}")
        logger.info(f"输出目录: {output_dir}")
        logger.info(f"强制覆盖: {force_overwrite}")
        logger.info("-" * 50)

        generator = APIGenerator(output_dir=output_dir)
        generated_files = generator.generate_apis_from_swagger(swagger_url, force_overwrite)

        logger.info("-" * 50)
        logger.info(f"共生成 {len(generated_files)} 个API接口文件")

        if generated_files:
            # 生成索引文件
            generator.generate_index_file(generated_files)

    elif command == "summary":
        har_file = "api_request.har"
        if len(sys.argv) > 2:
            har_file = sys.argv[2]

        parser = HARParser()
        parser.print_api_summary(har_file)

    elif command == "help":
        logger.info("har2pytest - API生成和更新工具")
        logger.info("=" * 50)
        logger.info("")
        logger.info("基本用法:")
        logger.info("  har2pytest <command> [arguments]")
        logger.info("")
        logger.info("支持的命令:")
        logger.info("  generate [har_file] [output_dir] [--overwrite]      从HAR文件生成API接口")
        logger.info("  testcase [har_file] [output_dir]                  从HAR文件生成步骤化pytest用例")
        logger.info("  testcase list_query [task_id] [har_file]           生成查询类参数化测试用例")
        logger.info("  testcase complex_scenario [task_id] [url] [har]  生成复杂场景流程测试用例")
        logger.info("  update [api_dir]                                  更新API文档信息")
        logger.info("  swagger <swagger_url> [output_dir] [--overwrite]  从Swagger文档生成API接口")
        logger.info("  summary [har_file]                                显示HAR文件摘要")
        logger.info("  help                                             显示此帮助信息")
        logger.info("  --help                                          显示此帮助信息")
        logger.info("")
        logger.info("参数说明:")
        logger.info("  --overwrite, -f                                 强制覆盖已存在的API文件")
        logger.info("")
        logger.info("示例:")
        logger.info("  har2pytest generate api_request.har api")
        logger.info("  har2pytest generate api_request.har api --overwrite  # 强制覆盖")
        logger.info("  har2pytest testcase api_request.har testcases")
        logger.info("  har2pytest update api")
        logger.info("  har2pytest swagger https://petstore.swagger.io/v2/api-docs api")
        logger.info("  har2pytest swagger https://petstore.swagger.io/v2/api-docs api --overwrite  # 强制覆盖")
        logger.info("  har2pytest summary api_request.har")
        logger.info("")
        logger.info("默认值:")
        logger.info("  HAR文件: api_request.har")
        logger.info("  输出目录: api")

    else:
        logger.info(f"未知命令: {command}")
        logger.info("使用 'har2pytest help' 查看帮助信息")


if __name__ == "__main__":
    main()

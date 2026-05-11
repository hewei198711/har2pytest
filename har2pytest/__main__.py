"""
har2pytest 命令行入口
"""

import argparse

from .api_generator import APIGenerator
from .config import APIConfig
from .har_generator import generate_api_files_from_har
from .har_parser import HARParser
from .logger import logger
from .swagger_handler import SwaggerHandler
from .testcase_generator import TestCaseGenerator


def main():
    """
    主函数 - 支持多种命令行操作模式
    """
    # 初始化配置（通过 get_config 触发，会自动缓存）
    APIConfig.get_config("BASE_URLS")

    # 创建主解析器
    parser = argparse.ArgumentParser(
        prog="har2pytest",
        description="har2pytest - HAR文件转pytest测试用例工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""示例用法:
  # 从HAR文件生成API接口文件
  har2pytest api api_request.har --output apis

  # 查看HAR文件摘要
  har2pytest summary api_request.har

  # 更新API文档信息
  har2pytest update apis

  # 生成查询类参数化测试用例
  har2pytest testcase api_request.har --pattern list_query --mark test_4291

  # 生成复杂场景测试用例
  har2pytest testcase api_request.har --pattern complex_scenario --url /api/user/login --mark test_4295
""",
    )

    # 创建子命令解析器
    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    # api 子命令
    api_parser = subparsers.add_parser("api", help="从HAR文件生成API接口文件", description="从HAR文件生成API接口文件")
    api_parser.add_argument("har_file", nargs="?", default="api_request.har", help="HAR文件路径")
    api_parser.add_argument("--output", "-o", default=APIConfig.DEFAULT_API_DIR(), help="输出目录")
    api_parser.add_argument("--overwrite", "-f", action="store_true", help="强制覆盖现有文件")

    # summary 子命令
    sum_parser = subparsers.add_parser(
        "summary", help="显示HAR文件的API请求摘要", description="显示HAR文件的API请求摘要"
    )
    sum_parser.add_argument("har_file", help="HAR文件路径")

    # update 子命令
    upd_parser = subparsers.add_parser(
        "update", help="更新现有API文件的文档信息", description="更新现有API文件的文档信息"
    )
    upd_parser.add_argument("api_dir", nargs="?", default=APIConfig.DEFAULT_API_DIR(), help="API文件目录")

    # testcase 子命令
    tc_parser = subparsers.add_parser(
        "testcase",
        help="生成测试用例",
        description="从HAR文件生成pytest测试用例",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""示例用法:
  # 生成查询类参数化测试用例（不传mark）
  har2pytest testcase api_request.har --pattern list_query

  # 生成查询类参数化测试用例（传mark）
  har2pytest testcase api_request.har --pattern list_query --mark test_4291

  # 生成复杂场景测试用例（不传mark）
  har2pytest testcase api_request.har --pattern complex_scenario --url /api/user/login

  # 生成复杂场景测试用例（传mark）
  har2pytest testcase api_request.har --pattern complex_scenario --url /api/user/login --mark test_4295
""",
    )
    tc_parser.add_argument("har_file", help="HAR文件路径")
    tc_parser.add_argument(
        "--pattern",
        "-p",
        default="simple",
        choices=["simple", "list_query", "complex_scenario"],
        help="测试用例模式: simple(通用测试)、list_query(查询类参数化) 或 complex_scenario(复杂场景)",
    )
    tc_parser.add_argument("--mark", "-m", help="测试标记（如 test_4291）")
    tc_parser.add_argument("--url", "-u", help="目标接口URL（complex_scenario模式必填）")
    tc_parser.add_argument("--output", "-o", default="testcases", help="输出目录")
    tc_parser.add_argument("--api-dir", default="apis", help="API文件目录")

    # swagger 子命令
    swagger_parser = subparsers.add_parser(
        "swagger",
        help="从Swagger文档生成API接口文件",
        description="从Swagger文档生成API接口文件",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""示例用法:
  # 从Swagger文档生成所有API文件
  har2pytest swagger https://petstore.swagger.io/v2/api-docs

  # 从Swagger文档生成API文件，指定输出目录
  har2pytest swagger https://petstore.swagger.io/v2/api-docs --output apis

  # 从Swagger文档生成API文件，强制覆盖
  har2pytest swagger https://petstore.swagger.io/v2/api-docs --overwrite

  # 从Swagger文档生成指定路径的API文件
  har2pytest swagger https://petstore.swagger.io/v2/api-docs --path /pet/{petId}
""",
    )
    swagger_parser.add_argument("swagger_url", help="Swagger文档URL")
    swagger_parser.add_argument("--output", "-o", default=APIConfig.DEFAULT_API_DIR(), help="输出目录")
    swagger_parser.add_argument("--overwrite", "-f", action="store_true", help="强制覆盖现有文件")
    swagger_parser.add_argument("--path", "-p", help="只生成指定的API路径（如 /pet/{petId}）")

    # 解析参数
    args = parser.parse_args()

    # 如果没有指定命令，默认使用 generate
    if args.command is None:
        args.command = "generate"
        args.har_file = "api_request.har"
        args.output = APIConfig.DEFAULT_API_DIR()
        args.overwrite = False

    # 执行对应的命令
    if args.command == "api":
        handle_api(args)
    elif args.command == "summary":
        handle_summary(args)
    elif args.command == "update":
        handle_update(args)
    elif args.command == "testcase":
        handle_testcase(args)
    elif args.command == "swagger":
        handle_swagger(args)
    elif args.command == "help":
        parser.print_help()
    else:
        logger.error(f"未知命令: {args.command}")
        parser.print_help()


def handle_api(args):
    """处理 api 命令"""
    har_file = args.har_file
    output_dir = args.output
    force_overwrite = args.overwrite

    logger.info(f"从HAR文件生成API接口文件: {har_file}")
    logger.info(f"输出目录: {output_dir}")
    logger.info(f"强制覆盖: {force_overwrite}")
    logger.info("-" * 50)

    api_generator = APIGenerator(output_dir)
    generated_files = generate_api_files_from_har(har_file, force_overwrite=force_overwrite, api_generator=api_generator)

    logger.info("-" * 50)
    logger.info(f"共生成 {len(generated_files)} 个API接口文件")

    if generated_files:
        api_generator.generate_index_file(generated_files)


def handle_summary(args):
    """处理 summary 命令"""
    har_file = args.har_file

    parser = HARParser()
    parser.print_api_summary(har_file)


def handle_update(args):
    """处理 update 命令"""
    api_dir = args.api_dir

    logger.info(f"更新API文件文档信息: {api_dir}")
    logger.info("-" * 50)

    api_generator = APIGenerator(api_dir)
    updated_count = api_generator.update_api_docs()

    logger.info("-" * 50)
    logger.info(f"共更新 {updated_count} 个API文件")


def handle_swagger(args):
    """处理 swagger 命令"""
    swagger_url = args.swagger_url
    output_dir = args.output
    force_overwrite = args.overwrite
    specific_path = args.path

    logger.info(f"从Swagger文档生成API接口文件: {swagger_url}")
    logger.info(f"输出目录: {output_dir}")
    logger.info(f"强制覆盖: {force_overwrite}")
    if specific_path:
        logger.info(f"只生成指定路径: {specific_path}")
    logger.info("-" * 50)

    api_generator = APIGenerator(output_dir)
    swagger_handler = SwaggerHandler(api_generator=api_generator)
    generated_files = swagger_handler.generate_apis_from_swagger(swagger_url, force_overwrite, specific_path)

    logger.info("-" * 50)
    logger.info(f"共生成 {len(generated_files)} 个API接口文件")

    if generated_files:
        api_generator.generate_index_file(generated_files)


def handle_testcase(args):
    """处理 testcase 命令"""
    har_file = args.har_file
    pattern = args.pattern
    task_id = args.mark
    target_url = args.url
    output_dir = args.output
    api_dir = args.api_dir

    # 如果 task_id 以 test_ 开头，去掉前缀
    if task_id and task_id.startswith("test_"):
        task_id = task_id[5:]

    if pattern == "simple":
        logger.info(f"生成通用测试用例: {har_file}")
        logger.info("-" * 50)

        generator = TestCaseGenerator(api_dir=api_dir, output_dir=output_dir)
        test_file = generator.generate_test_case_from_har(har_file)

        logger.info("-" * 50)
        if test_file:
            logger.info(f"成功生成测试用例文件: {test_file.replace('\\', '/')}")
        else:
            logger.info("生成测试用例文件失败")

    elif pattern == "list_query":
        logger.info(f"生成查询类参数化测试用例: {har_file}")
        logger.info(f"任务ID: {task_id}")
        logger.info("-" * 50)

        generator = TestCaseGenerator(api_dir=api_dir, output_dir=output_dir)
        test_files = generator.generate_parametrized_list_testcases(har_file, task_id)

        logger.info("-" * 50)
        if test_files:
            logger.info(f"成功生成 {len(test_files)} 个测试用例文件:")
            for test_file in test_files:
                logger.info(f"  - {test_file}")
        else:
            logger.info("生成测试用例文件失败")

    elif pattern == "complex_scenario":
        # 验证必填参数
        if not target_url:
            logger.error("错误: complex_scenario 模式必须指定 --url 参数")
            logger.error("使用示例: har2pytest testcase api.har --pattern complex_scenario --url /api/user/login")
            return

        logger.info(f"生成复杂场景测试用例: {har_file}")
        logger.info(f"任务ID: {task_id}")
        logger.info(f"目标接口: {target_url}")
        logger.info("-" * 50)

        generator = TestCaseGenerator(api_dir=api_dir, output_dir=output_dir)
        test_file = generator.generate_scenario_testcase(har_file, target_url, task_id)

        logger.info("-" * 50)
        if test_file:
            logger.info(f"成功生成测试用例文件: {test_file.replace('\\', '/')}")
        else:
            logger.info("生成测试用例文件失败")


if __name__ == "__main__":
    main()

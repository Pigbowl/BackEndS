#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试问题收到确认邮件功能
"""

import sys
import os

# 添加当前目录到系统路径，解决模块导入问题
sys.path.append(os.path.abspath('.'))

from Python_S.emailing import sender

# 测试问题数据
test_issue_data = {
    'Name': '测试用户',
    'Type': '功能建议',
    'Title': '关于改进用户界面的建议',
    'Description': '我希望能改进用户界面，使其更加简洁易用，特别是在移动端的体验。'
}

print("测试问题收到确认邮件功能...")
try:
    # 调用生成内容的函数
    content = sender.get_issue_recieve_confirm_content(test_issue_data)
    
    # 验证内容是否包含必要信息
    assert '测试用户' in content, "用户名未正确插入"
    assert '功能建议' in content, "问题类型未正确插入"
    assert '关于改进用户界面的建议' in content, "问题标题未正确插入"
    assert '我希望能改进用户界面' in content, "问题描述未正确插入"
    assert '问题收到确认' in content, "邮件标题未正确插入"
    assert '2日之内进行处理' in content, "处理时间提示未正确插入"
    
    print("问题收到确认邮件内容生成成功！")
    print("\n邮件内容预览（前500字符）：")
    print(content[:500] + "...")
    print("=" * 50)
    
    print("\n测试完成！问题收到确认邮件功能正常工作。")
    
except Exception as e:
    print(f"测试失败：{str(e)}")
    import traceback
    traceback.print_exc()

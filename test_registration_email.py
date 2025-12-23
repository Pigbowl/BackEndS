#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试注册成功确认邮件功能
"""

import sys
import os

# 添加当前目录到系统路径，解决模块导入问题
sys.path.append(os.path.abspath('.'))

# 从emailing模块导入sender对象和全局函数
from Python_S.emailing import sender, send_single_email

# 测试用户数据
test_user_data = {
    'Name': '测试用户',
    'Email': 'test@example.com',
    'Password': 'Test123456'
}

print("测试注册成功确认邮件内容生成...")
try:
    # 调用生成内容的函数
    content = sender.get_registration_confirmation_content(test_user_data)
    
    # 验证内容是否包含必要信息
    assert '测试用户' in content, "用户名未正确插入"
    assert 'test@example.com' in content, "用户邮箱未正确插入"
    assert 'Test123456' in content, "用户密码未正确插入"
    assert '登录达客科技' in content, "登录链接未正确插入"
    
    print("注册成功确认邮件内容生成成功！")
    print("\n邮件内容预览：")
    print("=" * 50)
    # 只打印前500个字符作为预览
    print(content[:500] + "...")
    print("=" * 50)
    
    # 测试send_single_email函数
    print("\n测试send_single_email函数接口...")
    # 注意：这里只是测试函数调用是否正常，不会实际发送邮件（因为没有真实的收件人邮箱）
    # 如果要实际发送邮件，请将收件人邮箱改为真实有效的邮箱
    result = send_single_email(
        recipient_email='test@example.com',
        email_type='registration_confirmation',
        user_data=test_user_data
    )
    print(f"send_single_email函数调用结果：{result}")
    print("测试完成！")
    
except Exception as e:
    print(f"测试失败：{str(e)}")
    import traceback
    traceback.print_exc()

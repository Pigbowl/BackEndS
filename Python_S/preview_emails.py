#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
预览所有邮件内容
"""

import sys
import os

# 添加当前目录到系统路径，解决模块导入问题
sys.path.append(os.path.abspath('.'))

from Python_S.emailing import sender

# 测试数据
test_user_data = {
    'Name': '测试用户',
    'Email': 'test@example.com',
    'Password': 'Test123456',
    'email': 'test@example.com'  # 用于admin_notification
}

# 创建一个HTML文件来预览所有邮件
preview_file = "email_preview.html"

with open(preview_file, 'w', encoding='utf-8') as f:
    f.write("""
    <html>
    <head>
        <meta charset="utf-8">
        <title>邮件内容预览</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f0f0f0;
                margin: 0;
                padding: 20px;
            }
            .email-container {
                background-color: white;
                border-radius: 8px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                margin-bottom: 30px;
                padding: 20px;
            }
            .email-header {
                background-color: #1a73e8;
                color: white;
                padding: 15px;
                border-radius: 6px;
                margin-bottom: 20px;
            }
            .email-content {
                border: 1px solid #e0e0e0;
                border-radius: 6px;
                padding: 20px;
                background-color: #fafafa;
            }
            h1 {
                text-align: center;
                color: #333;
            }
            h2 {
                margin-top: 0;
            }
            iframe {
                width: 100%;
                height: 600px;
                border: 1px solid #ddd;
                border-radius: 4px;
            }
        </style>
    </head>
    <body>
        <h1>达客科技邮件内容预览</h1>
    """)
    
    # 生成并预览每种邮件类型
    email_types = [
        ("product_update", "产品上线提醒", sender.get_product_update_content),
        ("subscription_confirm", "订阅确认", sender.get_subscription_confirm_content),
        ("admin_notification", "管理员提醒", lambda: sender.get_admin_notification_content(test_user_data)),
        ("registration_confirmation", "注册成功确认", lambda: sender.get_registration_confirmation_content(test_user_data))
    ]
    
    for email_type, title, content_func in email_types:
        print(f"正在生成 {title} 邮件内容...")
        try:
            # 生成邮件内容
            content = content_func()
            
            # 保存单个邮件的HTML文件
            single_file = f"{email_type}_preview.html"
            with open(single_file, 'w', encoding='utf-8') as single_f:
                single_f.write(content)
            
            # 在预览页面中添加该邮件
            f.write(f"""
            <div class="email-container">
                <div class="email-header">
                    <h2>{title} ({email_type})</h2>
                </div>
                <div class="email-content">
                    <h3>邮件内容预览：</h3>
                    <iframe src="{single_file}"></iframe>
                    <p style="margin-top: 10px;">可以直接打开文件查看：<a href="{single_file}" target="_blank">{single_file}</a></p>
                </div>
            </div>
            """)
            
            print(f"{title} 邮件内容已生成并保存到 {single_file}")
            
        except Exception as e:
            print(f"生成 {title} 邮件内容失败：{str(e)}")
            import traceback
            traceback.print_exc()
    
    f.write("""
    </body>
    </html>
    """)

print(f"\n所有邮件内容预览已生成并保存到 {preview_file}")
print("您可以直接在浏览器中打开该文件查看所有邮件的预览效果。")

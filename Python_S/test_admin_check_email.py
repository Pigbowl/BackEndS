#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试管理员检查通知邮件功能
"""

import sys
import os
import datetime
import base64

# 简化的邮件内容生成测试，避免依赖其他模块

# 测试数据
test_issue_data = {
    'UserName': '测试用户',
    'Type': '功能建议',
    'Category': '关于导航功能的改进建议',
    'Description': '我希望导航功能能够添加实时路况预测功能，这样可以提前规划路线，避开拥堵路段。'
}

# 函数：将图片转换为base64数据URL
def image_to_base64(image_path):
    try:
        full_path = os.path.join(r'c:\Users\宋嘉玮\OneDrive\Desktop\BackEndS', image_path)
        if os.path.exists(full_path):
            with open(full_path, "rb") as img_file:
                # 读取图片文件并转换为base64
                img_base64 = base64.b64encode(img_file.read()).decode('utf-8')
                # 根据文件扩展名确定MIME类型
                ext = os.path.splitext(image_path)[1].lower()
                mime_type = f"image/{ext[1:]}" if ext else "image/png"
                return f"data:{mime_type};base64,{img_base64}"
    except Exception as e:
        print(f"转换图片 {image_path} 为base64时出错: {e}")
    # 如果转换失败，返回空字符串
    return ""

# 测试邮件内容生成
print("开始测试管理员检查通知邮件功能...")

try:
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 转换图片为base64
    logo_base64 = image_to_base64("logo.png")
    darkerduck_base64 = image_to_base64("darkerduck.png")
    
    # 生成邮件内容
    email_content = f"""
    <html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
        <style>
            body {{ font-family: 'Microsoft YaHei', Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px; background-color: #f8f9fa; }}
            .container {{ background-color: white; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); padding: 30px; }}
            .header {{ text-align: center; padding-bottom: 20px; border-bottom: 2px solid #e7f0fd; margin-bottom: 20px; }}
            .logo {{ width: 80px; height: 80px; margin-bottom: 15px; }}
            h2 {{ color: #d93025; margin-top: 0; font-weight: bold; }}
            .issue-info {{ background-color: #fff3f3; border: 1px solid #ffcccc; padding: 20px; border-radius: 4px; margin: 20px 0; }}
            .info-item {{ margin-bottom: 15px; }}
            .info-label {{ font-weight: bold; color: #555; display: inline-block; width: 100px; }}
            .urgent-note {{ background-color: #fff3f3; border-left: 4px solid #d93025; padding: 15px; margin: 20px 0; }}
            .footer {{ margin-top: 30px; font-size: 12px; color: #666; text-align: center; }}
            .time-info {{ font-size: 12px; color: #666; text-align: right; margin-top: 20px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <!-- 使用base64数据URL嵌入图片 -->
                {f'<img src="{logo_base64}" alt="达客科技" class="logo" width="80" height="80"/>' if logo_base64 else '<h1 style="color: #1a73e8; margin: 0; font-size: 36px;">达客科技</h1>'}
                <h2>【紧急通知】收到新的问题反馈，需尽快处理</h2>
            </div>
            
            <p>尊敬的管理员：</p>
            
            <p>有新用户提交了问题反馈，请尽快查看并处理！</p>
            
            <div class="issue-info">
                <div class="info-item">
                    <span class="info-label">提交用户：</span>
                    <span>{test_issue_data.get('UserName', '未知用户')}</span>
                </div>
                <div class="info-item">
                    <span class="info-label">问题类型：</span>
                    <span>{test_issue_data.get('Type', '未知类型')}</span>
                </div>
                <div class="info-item">
                    <span class="info-label">问题标题：</span>
                    <span>{test_issue_data.get('Category', '无标题')}</span>
                </div>
                <div class="info-item">
                    <span class="info-label">问题描述：</span>
                    <span>{test_issue_data.get('Description', '无描述')}</span>
                </div>
                <div class="info-item">
                    <span class="info-label">提交时间：</span>
                    <span>{current_time}</span>
                </div>
            </div>
            
            <div class="urgent-note">
                <p style="color: #d93025; font-weight: bold; margin: 0;">⚠️ 紧急提醒：</p>
                <p style="margin: 5px 0 0 0;">请务必在收到此邮件后的24小时内查看并处理该问题，确保用户体验和服务质量。</p>
            </div>
            
            <!-- 添加带图片的导向按钮，使用base64数据URL或emoji -->
            <div style="text-align: center; margin: 20px 0;">
                <a href="http://thedarker-tech.com/admin" style="display: inline-flex; align-items: center; background-color: #d93025; color: white; text-decoration: none; padding: 12px 25px; border-radius: 4px; font-weight: bold; gap: 10px; font-size: 16px;">
                    立即查看问题
                    {f'<img src="{darkerduck_base64}" alt="达客鸭" style="width: 24px; height: 24px; vertical-align: middle;"/>' if darkerduck_base64 else '<span style="font-size: 18px;">🚨</span>'}
                </a>
            </div>
            
            <div class="time-info">
                <p>发送时间：{current_time}</p>
                <p>发件人：达客小助手</p>
            </div>
            
            <hr>
            <div class="footer">
                <p>此邮件由达客科技系统自动发送，请勿回复。</p>
                <p>© 2025 达客科技. 保留所有权利。</p>
            </div>
        </div>
        </body>
        </html>
        """
    
    print("\n✅ 邮件内容生成成功！")
    
    # 保存邮件内容到文件，方便查看
    with open('admin_check_email_test.html', 'w', encoding='utf-8') as f:
        f.write(email_content)
    print("✅ 邮件内容已保存到 admin_check_email_test.html")
    
    print("\n📧 邮件预览：")
    print(email_content[:500] + "...")  # 只显示前500个字符
    
    print("\n🎉 测试完成！")
    
except Exception as e:
    print(f"\n❌ 测试失败：{str(e)}")
    import traceback
    traceback.print_exc()

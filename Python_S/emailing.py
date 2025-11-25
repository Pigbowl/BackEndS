
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import smtplib
import ssl
import re
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.utils import formataddr
import datetime

# 配置日志记录
logging.basicConfig(
    filename='email_sender.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def send_email(bcc_recipients=None):
    # 邮件服务器配置
    smtp_server = "smtp.exmail.qq.com"
    port = 465  # SSL端口
    
    # 发件人信息
    sender_email = "darkerAssistance@thedarker-tech.com"
    sender_password = "wtgYJBBMT4Kddjab"
    sender_name = "Darker Assistance"
    
    # 收件人信息
    receiver_email = "song-jiawei@outlook.com"
    
    # 确保bcc_recipients是一个列表
    if bcc_recipients is None:
        bcc_recipients = ["1273880613@qq.com","shuiguo378060679@qq.com","875361542@qq.com"]
    
    # 验证邮箱格式
    def is_valid_email(email):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email)
    
    # 验证主要收件人邮箱
    if not is_valid_email(receiver_email):
        error_msg = f"无效的收件人邮箱地址: {receiver_email}"
        logging.error(error_msg)
        print(f"错误: {error_msg}")
        return False
    
    # 验证BCC收件人邮箱
    valid_bcc = []
    invalid_bcc = []
    for email in bcc_recipients:
        if is_valid_email(email):
            valid_bcc.append(email)
        else:
            invalid_bcc.append(email)
    
    if invalid_bcc:
        warning_msg = f"以下BCC收件人邮箱地址无效，将被忽略: {', '.join(invalid_bcc)}"
        logging.warning(warning_msg)
        print(f"警告: {warning_msg}")
    
    bcc_recipients = valid_bcc
    logging.info(f"准备发送邮件，主要收件人: {receiver_email}, BCC收件人数量: {len(bcc_recipients)}")
    
    try:
        # 创建MIME多部分消息
        message = MIMEMultipart()
        message["From"] = formataddr((str(Header(sender_name, 'utf-8')), sender_email))
        message["To"] = receiver_email
        message["Subject"] = Header("【更新提示】达客智驾领航员更新了", 'utf-8')
        
        # 邮件正文内容
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 定义更新版本号
        version = "2.3.5"
        
        # 构建BCC收件人显示部分
        bcc_display = ""
        if bcc_recipients:
            bcc_display = f"<p>BCC收件人：{', '.join(bcc_recipients)}</p>"
        
        email_content = f"""
        <html>
        <head>
            <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
            <style>
                body {{
                    font-family: 'Microsoft YaHei', Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                    background-color: #f8f9fa;
                }}
                .container {{
                    background-color: white;
                    border-radius: 8px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                    padding: 30px;
                }}
                .header {{
                    text-align: center;
                    padding-bottom: 20px;
                    border-bottom: 2px solid #e7f0fd;
                    margin-bottom: 20px;
                }}
                .logo {{
                    width: 80px;
                    height: 80px;
                    margin-bottom: 15px;
                }}
                h2 {{
                    color: #1a73e8;
                    margin-top: 0;
                }}
                h3 {{
                    color: #333;
                    border-left: 4px solid #1a73e8;
                    padding-left: 10px;
                }}
                .version {{ color: #d93025; }}
                ul {{
                    padding-left: 20px;
                }}
                li {{
                    margin-bottom: 8px;
                    position: relative;
                    padding-left: 5px;
                }}
                li:before {{
                    content: '✓';
                    color: #1a73e8;
                    position: absolute;
                    left: -18px;
                }}
                .action-button {{
                    display: inline-block;
                    background-color: #1a73e8;
                    color: white;
                    text-decoration: none;
                    padding: 10px 20px;
                    border-radius: 4px;
                    margin: 15px 0;
                    font-weight: bold;
                    transition: background-color 0.3s;
                }}
                .action-button:hover {{
                    background-color: #1557b0;
                }}
                .footer {{
                    margin-top: 30px;
                    font-size: 12px;
                    color: #666;
                    text-align: center;
                }}
                .time-info {{
                    font-size: 12px;
                    color: #666;
                    text-align: right;
                    margin-top: 20px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <!-- 使用SVG作为公司标志 -->
                    <svg class="logo" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
                        <rect width="100" height="100" rx="10" fill="#1a73e8"/>
                        <path d="M25,40 L75,40 L75,60 L25,60 Z" fill="white" rx="3"/>
                        <circle cx="50" cy="50" r="15" fill="#1a73e8"/>
                        <path d="M35,50 L65,50" stroke="white" stroke-width="6" stroke-linecap="round"/>
                    </svg>
                    <h2>【更新提示】达客智驾领航员更新了</h2>
                </div>
                
                <p>尊敬的用户，达客科技已更新至 <strong class="version">{version}</strong> 版本。</p>
                
                <h3>本次更新内容：</h3>
                <ul>
                    <li>优化了导航算法，提升了在复杂路况下的导航准确性</li>
                    <li>新增智能语音助手功能，支持更多自然语言指令</li>
                    <li>改进了用户界面，提升了整体视觉体验和交互流畅度</li>
                    <li>修复了已知的稳定性问题，增强了系统可靠性</li>
                    <li>增加了实时路况信息更新频率，提供更精准的交通状况</li>
                </ul>
                
                <p>查看完整更新说明：</p>
                <a href="http://thedarker-tech.com" class="action-button">访问达客科技官网</a>
                
                <div class="time-info">
                    <p>发送时间：{current_time}</p>
                    <p>发件人：{sender_name}</p>
                </div>
                
                <hr>
                <div class="footer">
                    <p>此邮件由达客科技系统自动发送，请勿回复。如有问题，请联系客服。</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # 添加HTML格式的正文
        html_part = MIMEText(email_content, 'html', 'utf-8')
        message.attach(html_part)
        
        # 创建SSL上下文
        context = ssl.create_default_context()
        
        # 创建完整的收件人列表（包括主要收件人和BCC收件人）
        all_recipients = [receiver_email] + bcc_recipients
        logging.info(f"准备发送邮件到以下收件人：主要收件人 - {receiver_email}, BCC收件人 - {', '.join(bcc_recipients) if bcc_recipients else '无'}")
        
        # 连接到SMTP服务器并发送邮件
        print("正在连接到邮件服务器...")
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            print("连接成功，正在登录...")
            server.login(sender_email, sender_password)
            print("登录成功，正在发送邮件...")
            server.sendmail(sender_email, all_recipients, message.as_string())
            print(f"邮件发送成功！已发送到 {len(all_recipients)} 个收件人")
            logging.info(f"邮件发送成功！已发送到 {len(all_recipients)} 个收件人")
            return True
            
    except smtplib.SMTPAuthenticationError:
        error_msg = "认证失败，请检查用户名和密码"
        logging.error(error_msg)
        print(f"错误：{error_msg}")
    except smtplib.SMTPException as e:
        error_msg = f"SMTP错误：{str(e)}"
        logging.error(error_msg)
        print(f"{error_msg}")
    except Exception as e:
        error_msg = f"发送邮件时发生错误：{str(e)}"
        logging.error(error_msg)
        print(f"{error_msg}")
    
    return False

if __name__ == "__main__":
    # 测试BCC功能，添加多个收件人到BCC列表
    # 注意：这里包含了一个有效邮箱和一个无效邮箱，用于测试错误处理功能
    test_bcc_recipients = ["1273880613@qq.com","shuiguo378060679@qq.com","875361542@qq.com"]
    
    print("开始测试邮件发送功能（含BCC）...")
    result = send_email(bcc_recipients=test_bcc_recipients)
    
    if result:
        print("测试完成，邮件发送成功！")
    else:
        print("测试完成，但邮件发送过程中出现错误。")


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
from Python_S.sql_operations import SQLOperations

# 配置日志记录
logging.basicConfig(
    filename='email_sender.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class EmailSender:
    def __init__(self):
        # 邮件服务器配置
        self.smtp_server = "smtp.exmail.qq.com"
        self.port = 465  # SSL端口
        
        # 发件人信息
        self.sender_email = "darkerAssistance@thedarker-tech.com"
        self.sender_password = "wtgYJBBMT4Kddjab"
        self.sender_name = "达客小助手"
    
    def is_valid_email(self, email):
        """
        验证邮箱格式
        """
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email)
    
    def get_all_user_emails(self):
        """
        从数据库读取所有用户的email
        """
        try:
            db = SQLOperations()
            users = db.read_data('user', columns=['email'])
            db.close()
            # 提取email列表
            emails = [user['email'] for user in users if user['email']]
            return emails
        except Exception as e:
            logging.error(f"从数据库读取用户邮箱失败: {str(e)}")
            print(f"错误: 从数据库读取用户邮箱失败: {str(e)}")
            return []
    
    def get_product_update_content(self):
        """
        生成产品上线提醒邮件内容
        """
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        version = "2.3.5"
        
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
                    <p>发件人：{self.sender_name}</p>
                </div>
                
                <hr>
                <div class="footer">
                    <p>此邮件由达客科技系统自动发送，请勿回复。如有问题，请联系客服。</p>
                </div>
            </div>
        </body>
        </html>
        """
        return email_content
    
    def get_subscription_confirm_content(self):
        """
        生成订阅确认邮件内容
        """
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
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
                .action-button {{
                    display: inline-block;
                    background-color: #1a73e8;
                    color: white;
                    text-decoration: none;
                    padding: 12px 25px;
                    border-radius: 4px;
                    margin: 20px 0;
                    font-weight: bold;
                    transition: background-color 0.3s;
                    font-size: 16px;
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
                    <h2>【订阅确认】达客科技</h2>
                </div>
                
                <p>尊敬的用户：</p>
                
                <p>感谢您订阅达客科技的最新动态！</p>
                
                <p>为了确保您能及时收到我们的产品更新、活动通知和行业资讯，请点击下方按钮完成订阅确认：</p>
                
                <center>
                    <a href="http://thedarker-tech.com" class="action-button">确认订阅</a>
                </center>
                
                <p>通过确认订阅，您将获得：</p>
                <ul>
                    <li>第一时间了解达客科技产品更新</li>
                    <li>获取独家技术资讯和行业洞察</li>
                    <li>参与专属活动和用户调研</li>
                    <li>享受优先体验新功能的权利</li>
                </ul>
                
                <p>如果您没有订阅我们的服务，或者这是一个误操作，请忽略此邮件。</p>
                
                <div class="time-info">
                    <p>发送时间：{current_time}</p>
                    <p>发件人：{self.sender_name}</p>
                </div>
                
                <hr>
                <div class="footer">
                    <p>此邮件由达客科技系统自动发送，请勿回复。如有问题，请联系客服。</p>
                </div>
            </div>
        </body>
        </html>
        """
        return email_content
    
    def send_email(self, mode="single", recipient_email=None, email_type="product_update"):
        """
        发送邮件
        
        Args:
            mode: 发送模式，"single"表示单发，"batch"表示群发
            recipient_email: 单发模式下的收件人邮箱
            email_type: 邮件类型，"product_update"表示产品上线提醒，"subscription_confirm"表示订阅确认
            
        Returns:
            bool: 发送是否成功
        """
        try:
            # 准备收件人列表
            if mode == "batch":
                # 群发模式：从数据库读取所有用户邮箱，使用BCC发送
                bcc_recipients = self.get_all_user_emails()
                # 群发邮件不需要主要收件人，使用发件人自己作为主要收件人
                receiver_email = self.sender_email
            elif mode == "single":
                # 单发模式：需要外部输入邮箱
                if not recipient_email:
                    error_msg = "单发模式下必须提供收件人邮箱"
                    logging.error(error_msg)
                    print(f"错误: {error_msg}")
                    return False
                if not self.is_valid_email(recipient_email):
                    error_msg = f"无效的收件人邮箱地址: {recipient_email}"
                    logging.error(error_msg)
                    print(f"错误: {error_msg}")
                    return False
                receiver_email = recipient_email
                bcc_recipients = []
            else:
                error_msg = f"无效的发送模式: {mode}，支持的模式为'single'和'batch'"
                logging.error(error_msg)
                print(f"错误: {error_msg}")
                return False
            
            # 验证BCC收件人邮箱
            valid_bcc = []
            invalid_bcc = []
            for email in bcc_recipients:
                if self.is_valid_email(email):
                    valid_bcc.append(email)
                else:
                    invalid_bcc.append(email)
            
            if invalid_bcc:
                warning_msg = f"以下BCC收件人邮箱地址无效，将被忽略: {', '.join(invalid_bcc)}"
                logging.warning(warning_msg)
                print(f"警告: {warning_msg}")
            
            bcc_recipients = valid_bcc
            
            # 准备邮件内容
            if email_type == "product_update":
                email_content = self.get_product_update_content()
                subject = Header("【更新提示】达客智驾领航员更新了", 'utf-8')
            elif email_type == "subscription_confirm":
                email_content = self.get_subscription_confirm_content()
                subject = Header("【订阅确认】达客科技", 'utf-8')
            else:
                error_msg = f"无效的邮件类型: {email_type}，支持的类型为'product_update'和'subscription_confirm'"
                logging.error(error_msg)
                print(f"错误: {error_msg}")
                return False
            
            logging.info(f"准备发送邮件，模式: {mode}, 类型: {email_type}, 主要收件人: {receiver_email}, BCC收件人数量: {len(bcc_recipients)}")
            
            # 创建MIME多部分消息
            message = MIMEMultipart()
            message["From"] = formataddr((str(Header(self.sender_name, 'utf-8')), self.sender_email))
            message["To"] = receiver_email
            message["Subject"] = subject
            
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
            with smtplib.SMTP_SSL(self.smtp_server, self.port, context=context) as server:
                print("连接成功，正在登录...")
                server.login(self.sender_email, self.sender_password)
                print("登录成功，正在发送邮件...")
                server.sendmail(self.sender_email, all_recipients, message.as_string())
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

# 创建全局实例，方便外部调用
sender = EmailSender()

# 外部调用接口
def send_batch_email(email_type="product_update"):
    """
    群发邮件接口
    
    Args:
        email_type: 邮件类型，"product_update"表示产品上线提醒，"subscription_confirm"表示订阅确认
        
    Returns:
        bool: 发送是否成功
    """
    return sender.send_email(mode="batch", email_type=email_type)

def send_single_email(recipient_email, email_type="product_update"):
    """
    单发邮件接口
    
    Args:
        recipient_email: 收件人邮箱
        email_type: 邮件类型，"product_update"表示产品上线提醒，"subscription_confirm"表示订阅确认
        
    Returns:
        bool: 发送是否成功
    """
    return sender.send_email(mode="single", recipient_email=recipient_email, email_type=email_type)

if __name__ == "__main__":
    # 测试代码
    print("开始测试邮件发送功能...")
    
    # 测试1：群发产品上线提醒
    print("\n测试1：群发产品上线提醒")
    # result1 = send_batch_email(email_type="product_update")
    # if result1:
    #     print("测试1成功！")
    # else:
    #     print("测试1失败！")
    
    # 测试2：单发订阅确认邮件
    print("\n测试2：单发订阅确认邮件")
    # result2 = send_single_email("test@example.com", email_type="subscription_confirm")
    # if result2:
    #     print("测试2成功！")
    # else:
    #     print("测试2失败！")
    
    print("\n测试完成！")

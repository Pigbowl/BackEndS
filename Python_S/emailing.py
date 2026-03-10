
import smtplib
import ssl
import re
import logging
import os
import base64
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.header import Header
from email.utils import formataddr
import datetime
from Python_S.sql_operations import SQLOperations

# global deploy_mode,server_product_config,server_operation_config,develop_product_config,develop_operation_config


with open('darker_config.json', 'r', encoding='utf-8') as f:
    config_data = json.load(f)
    deploy_mode = config_data.get('deploy_mode', 'test')  # 默认值为'test'
    server_product_config = config_data.get('server_product_config')
    server_operation_config = config_data.get('server_operation_config')
    develop_product_config = config_data.get('develop_product_config')
    develop_operation_config = config_data.get('develop_operation_config')
    admin_email = config_data.get('admin_email')
    sender_email = config_data.get('sender_email')
    sender_password = config_data.get('sender_password')
    smtp_server = config_data.get('smtp_server')
    port = config_data.get('port')
    sender_name = config_data.get('sender_name')
    darker_url = config_data.get('darker_url')


# 配置日志记录
logging.basicConfig(
    filename='email_sender.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class EmailSender:
    def __init__(self):
        # 邮件服务器配置
        self.smtp_server = smtp_server
        self.port = port  # SSL端口
        
        # 发件人信息
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.sender_name = sender_name
    
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
            if deploy_mode == 'test':
                database_config = develop_operation_config
            else:
                database_config = server_operation_config
            db = SQLOperations(database_config)
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
        
        # 函数：将图片转换为base64数据URL
        def image_to_base64(image_path):
            try:
                full_path = os.path.join('c:\\Users\\宋嘉玮\\OneDrive\\Desktop\\BackEndS', image_path)
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
        
        # 转换图片为base64
        logo_base64 = image_to_base64("logo.png")
        darkerduck_base64 = image_to_base64("darkerduck.png")
        
        email_content = f"""
        <html>
        <head>
            <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
            <style>
                body {{ font-family: 'Microsoft YaHei', Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px; background-color: #f8f9fa; }}
                .container {{ background-color: white; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); padding: 30px; }}
                .header {{ text-align: center; padding-bottom: 20px; border-bottom: 2px solid #e7f0fd; margin-bottom: 20px; }}
                .logo {{ width: 80px; height: 80px; margin-bottom: 15px; }}
                h2 {{ color: #1a73e8; margin-top: 0; }}
                h3 {{ color: #333; border-left: 4px solid #1a73e8; padding-left: 10px; }}
                .version {{ color: #d93025; }}
                ul {{ padding-left: 20px; }}
                li {{ margin-bottom: 8px; position: relative; padding-left: 5px; }}
                li:before {{ content: '✓'; color: #1a73e8; position: absolute; left: -18px; }}
                .footer {{ margin-top: 30px; font-size: 12px; color: #666; text-align: center; }}
                .time-info {{ font-size: 12px; color: #666; text-align: right; margin-top: 20px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <!-- 使用base64数据URL嵌入图片 -->
                    {f'<img src="{logo_base64}" alt="达客科技" class="logo" width="80" height="80"/>' if logo_base64 else '<h1 style="color: #1a73e8; margin: 0; font-size: 36px;">达客科技</h1>'}
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
                <!-- 添加带图片的导向按钮，使用base64数据URL或emoji -->
                <div style="text-align: center; margin: 20px 0;">
                    <a href="{darker_url}" style="display: inline-flex; align-items: center; background-color: #1a73e8; color: white; text-decoration: none; padding: 12px 20px; border-radius: 4px; font-weight: bold; gap: 10px;">
                        访问达客科技官网
                        {f'<img src="{darkerduck_base64}" alt="达客鸭" style="width: 24px; height: 24px; vertical-align: middle;"/>' if darkerduck_base64 else '<span style="font-size: 18px;">🚀</span>'}
                    </a>
                </div>
                
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
    
    def get_subscription_confirm_content(self,user_data):
        """
        生成订阅通知邮件内容
        """
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # 函数：将图片转换为base64数据URL
        def image_to_base64(image_path):
            try:
                full_path = os.path.join('c:\\Users\\宋嘉玮\\OneDrive\\Desktop\\BackEndS', image_path)
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
        
        # 转换图片为base64
        logo_base64 = image_to_base64("logo.png")
        darkerduck_base64 = image_to_base64("darkerduck.png")
        
        email_content = f"""
        <html>
        <head>
            <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
            <style>
                body {{ font-family: 'Microsoft YaHei', Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px; background-color: #f8f9fa; }}
                .container {{ background-color: white; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); padding: 30px; }}
                .header {{ text-align: center; padding-bottom: 20px; border-bottom: 2px solid #e7f0fd; margin-bottom: 20px; }}
                .logo {{ width: 80px; height: 80px; margin-bottom: 15px; }}
                h2 {{ color: #1a73e8; margin-top: 0; }}
                .footer {{ margin-top: 30px; font-size: 12px; color: #666; text-align: center; }}
                .time-info {{ font-size: 12px; color: #666; text-align: right; margin-top: 20px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <!-- 使用base64数据URL嵌入图片 -->
                    {f'<img src="{logo_base64}" alt="达客科技" class="logo" width="80" height="80"/>' if logo_base64 else '<h1 style="color: #1a73e8; margin: 0; font-size: 36px;">达客科技</h1>'}
                    <h2>【订阅通知】达客科技</h2>
                </div>
                
                <p>尊敬的{user_data["Name"]}用户：</p>
                
                <p>感谢您订阅达客科技的最新动态！</p>
                
                <p>您已成功订阅我们的服务，将及时收到我们的产品更新、活动通知和行业资讯。</p>
                
                <!-- 添加带图片的导向按钮，使用base64数据URL或emoji -->
                <div style="text-align: center; margin: 20px 0;">
                    <a href="{darker_url}" style="display: inline-flex; align-items: center; background-color: #1a73e8; color: white; text-decoration: none; padding: 12px 25px; border-radius: 4px; font-weight: bold; gap: 10px; font-size: 16px;">
                        访问达客科技官网
                        {f'<img src="{darkerduck_base64}" alt="达客鸭" style="width: 24px; height: 24px; vertical-align: middle;"/>' if darkerduck_base64 else '<span style="font-size: 18px;">✅</span>'}
                    </a>
                </div>
                
                <p>通过订阅，您将获得：</p>
                <ul>
                    <li>第一时间了解达客科技产品更新</li>
                    <li>获取独家技术资讯和行业洞察</li>
                    <li>参与专属活动和用户调研</li>
                    <li>享受优先体验新功能的权利</li>
                </ul>
                
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
        
    def get_admin_notification_content(self, user_data, notiftype="subscribe"):
        """
        生成管理员提醒邮件内容
        
        Args:
            user_data: 用户数据，包含用户名和邮箱
            notiftype: 通知类型，"subscribe"表示有人订阅，"registration"表示有人注册
        """
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 函数：将图片转换为base64数据URL
        def image_to_base64(image_path):
            try:
                full_path = os.path.join('c:\\Users\\宋嘉玮\\OneDrive\\Desktop\\BackEndS', image_path)
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
        
        # 转换图片为base64
        logo_base64 = image_to_base64("logo.png")
        darkerduck_base64 = image_to_base64("darkerduck.png")
        
        # 根据通知类型设置标题和内容
        if notiftype == "registration":
            title = "有人注册"
            action = "注册了"
            subject = "【注册通知】有人注册了达客科技服务"
        else:  # 默认subscribe
            title = "有人订阅"
            action = "订阅了"
            subject = "【订阅通知】有人订阅了达客科技服务"
        
        email_content = f"""
        <html>
        <head>
            <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
            <style>
                body {{ font-family: 'Microsoft YaHei', Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px; background-color: #f8f9fa; }}
                .container {{ background-color: white; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); padding: 30px; }}
                .header {{ text-align: center; padding-bottom: 20px; border-bottom: 2px solid #e7f0fd; margin-bottom: 20px; }}
                .logo {{ width: 80px; height: 80px; margin-bottom: 15px; }}
                h2 {{ color: #1a73e8; margin-top: 0; }}
                .user-info {{ background-color: #f0f4f8; padding: 15px; border-radius: 4px; margin: 20px 0; }}
                .info-item {{ margin-bottom: 10px; }}
                .info-label {{ font-weight: bold; color: #555; display: inline-block; width: 80px; }}
                .footer {{ margin-top: 30px; font-size: 12px; color: #666; text-align: center; }}
                .time-info {{ font-size: 12px; color: #666; text-align: right; margin-top: 20px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <!-- 使用base64数据URL嵌入图片 -->
                    {f'<img src="{logo_base64}" alt="达客科技" class="logo" width="80" height="80"/>' if logo_base64 else '<h1 style="color: #1a73e8; margin: 0; font-size: 36px;">达客科技</h1>'}
                    <h2>{subject}</h2>
                </div>
                
                <p>管理员您好，</p>
                
                <p>有新用户{action}达客科技服务，以下是用户信息：</p>
                
                <div class="user-info">
                    <div class="info-item">
                        <span class="info-label">用户名：</span>
                        <span>{user_data['Name']}</span>
                    </div>
                    <div class="info-item">
                        <span class="info-label">邮箱：</span>
                        <span>{user_data.get('email') or user_data.get('Email')}</span>
                    </div>
                    <div class="info-item">
                        <span class="info-label">时间：</span>
                        <span>{current_time}</span>
                    </div>
                </div>
                
                <p>请及时查看并处理。</p>
                
                <div class="time-info">
                    <p>发送时间：{current_time}</p>
                    <p>发件人：{self.sender_name}</p>
                </div>
                
                <hr>
                <div class="footer">
                    <p>此邮件由达客科技系统自动发送，请勿回复。</p>
                </div>
            </div>
        </body>
        </html>
        """
        return email_content
    
    def get_issue_recieve_confirm_content(self, issuedata):
        """
        生成问题收到确认邮件内容
        
        Args:
            issuedata: 问题数据，包含用户名、问题标题、问题类型和问题描述
        """
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 函数：将图片转换为base64数据URL
        def image_to_base64(image_path):
            try:
                full_path = os.path.join('c:\\Users\\宋嘉玮\\OneDrive\\Desktop\\BackEndS', image_path)
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
        
        # 转换图片为base64
        logo_base64 = image_to_base64("logo.png")
        darkerduck_base64 = image_to_base64("darkerduck.png")
        
        email_content = f"""
        <html>
        <head>
            <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
            <style>
                body {{ font-family: 'Microsoft YaHei', Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px; background-color: #f8f9fa; }}
                .container {{ background-color: white; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); padding: 30px; }}
                .header {{ text-align: center; padding-bottom: 20px; border-bottom: 2px solid #e7f0fd; margin-bottom: 20px; }}
                .logo {{ width: 80px; height: 80px; margin-bottom: 15px; }}
                h2 {{ color: #1a73e8; margin-top: 0; }}
                .issue-info {{ background-color: #f0f4f8; padding: 20px; border-radius: 4px; margin: 20px 0; }}
                .info-item {{ margin-bottom: 15px; }}
                .info-label {{ font-weight: bold; color: #555; display: inline-block; width: 100px; }}
                .footer {{ margin-top: 30px; font-size: 12px; color: #666; text-align: center; }}
                .time-info {{ font-size: 12px; color: #666; text-align: right; margin-top: 20px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <!-- 使用base64数据URL嵌入图片 -->
                    {f'<img src="{logo_base64}" alt="达客科技" class="logo" width="80" height="80"/>' if logo_base64 else '<h1 style="color: #1a73e8; margin: 0; font-size: 36px;">达客科技</h1>'}
                    <h2>【问题收到确认】您的问题已收到</h2>
                </div>
                
                <p>尊敬的{issuedata['UserName']}先生/女士：</p>
                
                <p>感谢您提交问题反馈！我们已经收到您的问题，并会在2日之内进行处理，决定是否修改或采纳。</p>
                
                <p>以下是您提交的问题信息：</p>
                
                <div class="issue-info">
                    <div class="info-item">
                        <span class="info-label">问题类型：</span>
                        <span>{issuedata['Type']}</span>
                    </div>
                    <div class="info-item">
                        <span class="info-label">问题标题：</span>
                        <span>{issuedata['Category']}</span>
                    </div>
                    <div class="info-item">
                        <span class="info-label">问题描述：</span>
                        <span>{issuedata['Description']}</span>
                    </div>
                </div>
                
                <p>再次感谢您对我们的支持！</p>
                
                <!-- 添加带图片的导向按钮，使用base64数据URL或emoji -->
                <div style="text-align: center; margin: 20px 0;">
                    <a href="{darker_url}" style="display: inline-flex; align-items: center; background-color: #1a73e8; color: white; text-decoration: none; padding: 12px 25px; border-radius: 4px; font-weight: bold; gap: 10px; font-size: 16px;">
                        访问达客科技官网
                        {f'<img src="{darkerduck_base64}" alt="达客鸭" style="width: 24px; height: 24px; vertical-align: middle;"/>' if darkerduck_base64 else '<span style="font-size: 18px;">✅</span>'}
                    </a>
                </div>
                
                <div class="time-info">
                    <p>发送时间：{current_time}</p>
                    <p>发件人：{self.sender_name}</p>
                </div>
                
                <hr>
                <div class="footer">
                    <p>此邮件由达客科技系统自动发送，请勿回复。如有问题，请联系客服。</p>
                    <p>© 2025 达客科技. 保留所有权利。</p>
                </div>
            </div>
        </body>
        </html>
        """
        return email_content
        
    def get_registration_confirmation_content(self, user_data):
        """
        生成用户注册成功确认邮件内容
        """
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 函数：将图片转换为base64数据URL
        def image_to_base64(image_path):
            try:
                full_path = os.path.join('c:\\Users\\宋嘉玮\\OneDrive\\Desktop\\BackEndS', image_path)
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
        
        # 转换图片为base64
        logo_base64 = image_to_base64("logo.png")
        darkerduck_base64 = image_to_base64("darkerduck.png")
        
        email_content = f"""
        <html>
        <head>
            <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
            <style>
                body {{ font-family: 'Microsoft YaHei', Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px; background-color: #f8f9fa; }}
                .container {{ background-color: white; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); padding: 30px; }}
                .header {{ text-align: center; padding-bottom: 20px; border-bottom: 2px solid #e7f0fd; margin-bottom: 20px; }}
                .logo {{ width: 80px; height: 80px; margin-bottom: 15px; }}
                h2 {{ color: #1a73e8; margin-top: 0; }}
                .login-info {{ background-color: #f0f4f8; padding: 20px; border-radius: 4px; margin: 20px 0; }}
                .info-item {{ margin-bottom: 15px; }}
                .info-label {{ font-weight: bold; color: #555; display: inline-block; width: 100px; }}
                .footer {{ margin-top: 30px; font-size: 12px; color: #666; text-align: center; }}
                .time-info {{ font-size: 12px; color: #666; text-align: right; margin-top: 20px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <!-- 使用base64数据URL嵌入图片 -->
                    {f'<img src="{logo_base64}" alt="达客科技" class="logo" width="80" height="80"/>' if logo_base64 else '<h1 style="color: #1a73e8; margin: 0; font-size: 36px;">达客科技</h1>'}
                    <h2>【注册成功】欢迎加入达客科技</h2>
                </div>
                
                <p>尊敬的{user_data['Name']}先生/女士：</p>
                
                <p>恭喜您成功注册达客科技服务！</p>
                
                <p>以下是您的账户信息：</p>
                
                <div class="login-info">
                    <div class="info-item">
                        <span class="info-label">用户名：</span>
                        <span>{user_data['Name']}</span>
                    </div>
                    <div class="info-item">
                        <span class="info-label">登录邮箱：</span>
                        <span>{user_data['Email']}</span>
                    </div>
                    <div class="info-item">
                        <span class="info-label">登录密码：</span>
                        <span>{user_data['Password']}</span>
                    </div>
                </div>
                
                <p>您可以使用<strong>用户名</strong>或<strong>邮箱地址</strong>进行登录。</p>
                
                <p>立即登录您的账户：</p>
                
                <!-- 添加带图片的导向按钮，使用base64数据URL或emoji -->
                <div style="text-align: center; margin: 20px 0;">
                    <a href="{darker_url}/pages/login.html" style="display: inline-flex; align-items: center; background-color: #1a73e8; color: white; text-decoration: none; padding: 12px 25px; border-radius: 4px; font-weight: bold; gap: 10px; font-size: 16px;">
                        登录达客科技
                        {f'<img src="{darkerduck_base64}" alt="达客鸭" style="width: 24px; height: 24px; vertical-align: middle;"/>' if darkerduck_base64 else '<span style="font-size: 18px;">🔑</span>'}
                    </a>
                </div>
                
                <p>如果您在使用过程中遇到任何问题，请随时联系我们的客服团队。</p>
                
                <div class="time-info">
                    <p>发送时间：{current_time}</p>
                    <p>发件人：{self.sender_name}</p>
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
        return email_content
    
    def get_admin_check_notif_content(self, issuedata):
        """
        生成管理员检查通知邮件内容
        
        Args:
            issuedata: 问题数据，包含用户名、问题标题、问题类型和问题描述
        """
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
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
        
        # 转换图片为base64
        logo_base64 = image_to_base64("logo.png")
        darkerduck_base64 = image_to_base64("darkerduck.png")
        
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
                        <span>{issuedata.get('UserName', '未知用户')}</span>
                    </div>
                    <div class="info-item">
                        <span class="info-label">问题类型：</span>
                        <span>{issuedata.get('Type', '未知类型')}</span>
                    </div>
                    <div class="info-item">
                        <span class="info-label">问题标题：</span>
                        <span>{issuedata.get('Category', '无标题')}</span>
                    </div>
                    <div class="info-item">
                        <span class="info-label">问题描述：</span>
                        <span>{issuedata.get('Description', '无描述')}</span>
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
                    <a href="{darker_url}" style="display: inline-flex; align-items: center; background-color: #d93025; color: white; text-decoration: none; padding: 12px 25px; border-radius: 4px; font-weight: bold; gap: 10px; font-size: 16px;">
                        立即查看问题
                        {f'<img src="{darkerduck_base64}" alt="达客鸭" style="width: 24px; height: 24px; vertical-align: middle;"/>' if darkerduck_base64 else '<span style="font-size: 18px;">🚨</span>'}
                    </a>
                </div>
                
                <div class="time-info">
                    <p>发送时间：{current_time}</p>
                    <p>发件人：{self.sender_name}</p>
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
        return email_content
    
    def send_email(self, mode="single", recipient_email=None, email_type="product_update", user_data=None, notiftype="subscribe"):
        """
        发送邮件
        
        Args:
            mode: 发送模式，"single"表示单发，"batch"表示群发
            recipient_email: 单发模式下的收件人邮箱
            email_type: 邮件类型，"product_update"表示产品上线提醒，"subscription_confirm"表示订阅通知，"admin_notification"表示管理员通知，"registration_confirmation"表示注册成功确认，"issue_recieve_confirm"表示问题收到确认
            custom_content: 自定义邮件内容（HTML格式），如果提供则忽略email_type
            custom_subject: 自定义邮件主题，如果提供则忽略email_type
            user_data: 用户数据，用于管理员通知邮件、注册成功确认邮件和问题收到确认邮件
            notiftype: 通知类型，"subscribe"表示有人订阅，"registration"表示有人注册，仅用于admin_notification类型
            
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
            
            # 准备邮件内容和主题
            if email_type == "product_update":
                email_content = self.get_product_update_content()
                subject = Header("【更新提示】达客智驾领航员更新了", 'utf-8')
            elif email_type == "subscription_notification":
                email_content = self.get_subscription_confirm_content(user_data)
                subject = Header("【订阅通知】达客科技", 'utf-8')
            elif email_type == "admin_notification":
                if not user_data:
                    error_msg = "admin_notification类型邮件必须提供user_data参数"
                    logging.error(error_msg)
                    print(f"错误: {error_msg}")
                    return False
                email_content = self.get_admin_notification_content(user_data, notiftype)
                # 根据notiftype设置主题
                if notiftype == "registration":
                    subject = Header("【注册通知】有人注册了达客科技服务", 'utf-8')
                else:
                    subject = Header("【订阅通知】有人订阅了达客科技服务", 'utf-8')
            elif email_type == "registration_confirmation":
                if not user_data:
                    error_msg = "registration_confirmation类型邮件必须提供user_data参数"
                    logging.error(error_msg)
                    print(f"错误: {error_msg}")
                    return False
                email_content = self.get_registration_confirmation_content(user_data)
                subject = Header("【注册成功】欢迎加入达客科技", 'utf-8')
            elif email_type == "issue_recieve_confirm":
                if not user_data:
                    error_msg = "issue_recieve_confirm类型邮件必须提供user_data参数"
                    logging.error(error_msg)
                    print(f"错误: {error_msg}")
                    return False
                email_content = self.get_issue_recieve_confirm_content(user_data)
                subject = Header("【问题收到确认】您的问题已收到", 'utf-8')
            elif email_type == "admin_check_notif":
                if not user_data:
                    error_msg = "admin_check_notif类型邮件必须提供user_data参数"
                    logging.error(error_msg)
                    print(f"错误: {error_msg}")
                    return False
                email_content = self.get_admin_check_notif_content(user_data)
                subject = Header("【紧急通知】收到新的问题反馈，需尽快处理", 'utf-8')
            else:
                error_msg = f"无效的邮件类型: {email_type}，支持的类型为'product_update'、'subscription_confirm'、'admin_notification'、'registration_confirmation'、'issue_recieve_confirm'和'admin_check_notif'"
                logging.error(error_msg)
                print(f"错误: {error_msg}")
                return False
            
            logging.info(f"准备发送邮件，模式: {mode}, 类型: {email_type}, 主要收件人: {receiver_email}, BCC收件人数量: {len(bcc_recipients)}")
            
            # 创建MIME多部分消息，支持混合内容（HTML和图片）
            message = MIMEMultipart('related')
            message["From"] = formataddr((str(Header(self.sender_name, 'utf-8')), self.sender_email))
            message["To"] = receiver_email
            message["Subject"] = subject
            
            # 创建HTML容器
            html_container = MIMEMultipart('alternative')
            message.attach(html_container)
            
            # 添加HTML格式的正文
            html_part = MIMEText(email_content, 'html', 'utf-8')
            html_container.attach(html_part)
            
            # 定义需要嵌入的图片
            images = [
                ('logo.png', 'logo'),
                ('darkerduck.png', 'darkerduck')
            ]
            
            for image_path, cid in images:
                # 检查图片文件是否存在
                full_path = os.path.join('c:\\Users\\宋嘉玮\\OneDrive\\Desktop\\BackEndS', image_path)
                if os.path.exists(full_path):
                    try:
                        # 读取图片文件并转换为base64
                        with open(full_path, 'rb') as f:
                            img_data = f.read()
                        
                        # 创建MIMEImage对象
                        image = MIMEImage(img_data)
                        
                        # 设置Content-ID，用于HTML中引用
                        image.add_header('Content-ID', f'<{cid}>')
                        
                        # 设置为内联图片
                        image.add_header('Content-Disposition', f'inline; filename="{image_path}"')
                        
                        # 添加到邮件中
                        message.attach(image)
                    except Exception as e:
                        logging.error(f"处理图片 {image_path} 时出错: {e}")
                else:
                    logging.warning(f"警告: 图片文件 {image_path} 不存在")
            
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

def send_single_email(recipient_email, email_type="product_update",user_data=None, notiftype="subscribe"):
    """
    单发邮件接口
    
    Args:
        recipient_email: 收件人邮箱
        email_type: 邮件类型，"product_update"表示产品上线提醒，"subscription_confirm"表示订阅通知，"admin_notification"表示管理员通知，"registration_confirmation"表示注册成功确认，"issue_recieve_confirm"表示问题收到确认，"admin_check_notif"表示管理员问题检查通知
        custom_content: 自定义邮件内容（HTML格式），如果提供则忽略email_type
        custom_subject: 自定义邮件主题，如果提供则忽略email_type
        user_data: 用户数据，用于管理员通知邮件、注册成功确认邮件和问题收到确认邮件
        notiftype: 通知类型，"subscribe"表示有人订阅，"registration"表示有人注册，仅用于admin_notification类型
        
    Returns:
        bool: 发送是否成功
    """
    return sender.send_email(
        mode="single", 
        recipient_email=recipient_email, 
        email_type=email_type,
        user_data=user_data,
        notiftype=notiftype
    )

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
    
    # 测试3：测试注册成功确认邮件内容生成
    print("\n测试3：生成注册成功确认邮件内容")
    test_user_data = {
        'Name': '测试用户',
        'Email': 'test@example.com',
        'Password': 'Test123456'
    }
    
    # 测试邮件内容生成
    try:
        content = sender.get_registration_confirmation_content(test_user_data)
        print("注册成功确认邮件内容生成成功！")
        print("邮件内容预览：")
        print(content[:500] + "...")  # 只显示前500个字符
    except Exception as e:
        print(f"生成注册成功确认邮件内容失败：{str(e)}")
    
    print("\n测试完成！")

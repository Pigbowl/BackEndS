#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import paramiko
import logging
import os

# 配置日志
logging.basicConfig(
    filename='remote_git_operations.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def connect_remote_server(server_ip, username, password, port=22):
    """
    连接到远程服务器
    
    Args:
        server_ip: 服务器IP地址
        username: SSH用户名
        password: SSH密码
        port: SSH端口，默认为22
    
    Returns:
        paramiko.SSHClient: SSH客户端对象，如果连接失败则返回None
    """
    try:
        # 创建SSH客户端
        ssh_client = paramiko.SSHClient()
        # 自动添加主机密钥
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        logging.info(f"正在连接到服务器 {server_ip}:{port}...")
        print(f"正在连接到服务器 {server_ip}:{port}...")
        
        # 连接到服务器
        ssh_client.connect(
            hostname=server_ip,
            port=port,
            username=username,
            password=password
        )
        
        logging.info(f"成功连接到服务器 {server_ip}")
        print(f"成功连接到服务器 {server_ip}")
        
        return ssh_client
        
    except paramiko.AuthenticationException:
        error_msg = f"认证失败，请检查用户名和密码"
        logging.error(error_msg)
        print(f"错误: {error_msg}")
        return None
    except paramiko.SSHException as e:
        error_msg = f"SSH连接错误: {str(e)}"
        logging.error(error_msg)
        print(f"错误: {error_msg}")
        return None
    except Exception as e:
        error_msg = f"连接服务器时发生错误: {str(e)}"
        logging.error(error_msg)
        print(f"错误: {error_msg}")
        return None

def execute_command(ssh_client, command):
    """
    在远程服务器上执行命令
    
    Args:
        ssh_client: SSH客户端对象
        command: 要执行的命令
    
    Returns:
        tuple: (stdout, stderr, exit_code)
    """
    try:
        logging.info(f"正在执行命令: {command}")
        print(f"执行命令: {command}")
        
        # 执行命令
        stdin, stdout, stderr = ssh_client.exec_command(command)
        
        # 获取退出码
        exit_code = stdout.channel.recv_exit_status()
        
        # 读取输出
        stdout_content = stdout.read().decode('utf-8')
        stderr_content = stderr.read().decode('utf-8')
        
        logging.info(f"命令执行完成，退出码: {exit_code}")
        
        # 打印输出
        if stdout_content:
            print(f"输出: {stdout_content}")
        if stderr_content:
            print(f"错误输出: {stderr_content}")
        
        return stdout_content, stderr_content, exit_code
        
    except Exception as e:
        error_msg = f"执行命令时发生错误: {str(e)}"
        logging.error(error_msg)
        print(f"错误: {error_msg}")
        return "", str(e), -1

def check_git_installed(ssh_client):
    """
    检查远程Windows服务器上是否安装了Git
    
    Args:
        ssh_client: SSH客户端对象
    
    Returns:
        bool: 如果Git已安装则返回True，否则返回False
    """
    # 在Windows上检查Git版本
    stdout, stderr, exit_code = execute_command(ssh_client, "git --version")
    
    # 即使stderr包含一些警告信息，如果能获取版本号也算安装成功
    combined_output = stdout + stderr
    if (exit_code == 0 or "git version" in combined_output) and "git version" in combined_output:
        git_version = combined_output.strip()
        logging.info(f"Git已安装: {git_version}")
        print(f"Git已安装: {git_version}")
        return True
    else:
        logging.warning("Git未安装在远程服务器上")
        print("警告: Git未安装在远程服务器上")
        return False

def git_clone(ssh_client, repo_url, target_dir):
    """
    在远程Windows服务器上克隆Git仓库
    
    Args:
        ssh_client: SSH客户端对象
        repo_url: GitHub仓库URL
        target_dir: 目标目录路径
    
    Returns:
        bool: 如果克隆成功则返回True，否则返回False
    """
    # 检查Git是否已安装
    if not check_git_installed(ssh_client):
        print("请先在服务器上安装Git")
        return False
    
    # 检查目标目录是否存在，如果不存在则创建（Windows命令）
    # 使用PowerShell创建目录，支持嵌套目录创建
    create_dir_command = f'powershell -Command "if(!(Test-Path \'{target_dir}\')) {{ New-Item -ItemType Directory -Force -Path \'{target_dir}\' }}"'
    stdout, stderr, exit_code = execute_command(ssh_client, create_dir_command)
    if exit_code != 0:
        logging.error(f"创建目录 {target_dir} 失败")
        return False
    
    # 执行Git克隆命令
    # 确保目标目录路径在Windows命令中正确处理（Windows环境不需要额外的单引号）
    clone_command = f"git clone {repo_url} {target_dir}"
    stdout, stderr, exit_code = execute_command(ssh_client, clone_command)
    
    if exit_code == 0:
        logging.info(f"成功克隆仓库 {repo_url} 到 {target_dir}")
        print(f"成功克隆仓库 {repo_url} 到 {target_dir}")
        return True
    else:
        logging.error(f"克隆仓库失败: {stderr}")
        print(f"克隆仓库失败: {stderr}")
        return False

def git_pull(ssh_client, repo_dir):
    """
    在远程Windows服务器上更新Git仓库
    
    Args:
        ssh_client: SSH客户端对象
        repo_dir: 仓库目录路径
    
    Returns:
        bool: 如果更新成功则返回True，否则返回False
    """
    # 检查Git是否已安装
    if not check_git_installed(ssh_client):
        print("请先在服务器上安装Git")
        return False
    
    # 执行Git pull命令（Windows版本，不需要额外的单引号）
    pull_command = f"cd {repo_dir} && git pull"
    stdout, stderr, exit_code = execute_command(ssh_client, pull_command)
    
    if exit_code == 0:
        logging.info(f"成功更新仓库 {repo_dir}")
        print(f"成功更新仓库 {repo_dir}")
        return True
    else:
        logging.error(f"更新仓库失败: {stderr}")
        print(f"更新仓库失败: {stderr}")
        return False

def main():
    """
    主函数，用于演示如何使用上述功能
    """
    # 服务器信息
    server_ip = "47.99.204.97"
    username = "Administrator"  # 假设使用root用户，根据实际情况修改
    password = "Sjw9@0613"
    
    # 固定的GitHub仓库URL
    github_repo = "https://github.com/Pigbowl/BackEndS.git"
    print(f"使用GitHub仓库URL: {github_repo}")
    # 固定的服务器目标目录
    target_dir = "C:\\Users\\Administrator\\Desktop\\darkerback"
    print(f"使用服务器目录: {target_dir}")
    
    # 连接服务器
    ssh_client = connect_remote_server(server_ip, username, password)
    
    if ssh_client:
        try:
            # 检查目标目录是否存在，并且是否为Git仓库
            check_dir_command = f'powershell -Command "Test-Path \"{target_dir}\\.git\""'
            stdout, stderr, exit_code = execute_command(ssh_client, check_dir_command)
            
            if "True" in stdout.strip():
                print(f"检测到目标目录 {target_dir} 已经是一个Git仓库，执行更新操作...")
                success = git_pull(ssh_client, target_dir)
                if success:
                    print("Git仓库更新操作完成！")
                else:
                    print("Git仓库更新操作失败！")
            else:
                # 检查目录是否存在但不是Git仓库
                check_exist_command = f'powershell -Command "Test-Path \"{target_dir}\""'
                stdout, stderr, exit_code = execute_command(ssh_client, check_exist_command)
                
                if "True" in stdout.strip():
                    print(f"目标目录 {target_dir} 已存在但不是Git仓库，先删除再克隆...")
                    # 删除已存在的目录
                    delete_dir_command = f'powershell -Command "Remove-Item -Path \"{target_dir}\" -Recurse -Force"'
                    stdout, stderr, exit_code = execute_command(ssh_client, delete_dir_command)
                    
                # 克隆仓库
                success = git_clone(ssh_client, github_repo, target_dir)
                
                if success:
                    print("Git仓库克隆操作完成！")
                else:
                    print("Git仓库克隆操作失败！")
                
        finally:
            # 关闭SSH连接
            ssh_client.close()
            logging.info("SSH连接已关闭")
            print("SSH连接已关闭")

if __name__ == "__main__":
    main()
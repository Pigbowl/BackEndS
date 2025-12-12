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
    create_dir_command = f'powershell -Command "if(!(Test-Path \'{target_dir}\')) {{ New-Item -ItemType Directory -Force -Path \'{target_dir}\' }}}}"'
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
    
    # 执行Git fetch获取最新代码，然后强制重置本地代码到远程main分支状态
    # 这样可以确保服务器代码完全遵循GitHub版本，忽略所有本地修改
    fetch_command = f"cd {repo_dir} && git fetch origin main"
    stdout, stderr, exit_code = execute_command(ssh_client, fetch_command)
    if exit_code != 0:
        logging.error(f"获取远程代码失败: {stderr}")
        print(f"获取远程代码失败: {stderr}")
        return False
    
    # 强制重置本地代码到远程main分支
    reset_command = f"cd {repo_dir} && git reset --hard origin/main"
    stdout, stderr, exit_code = execute_command(ssh_client, reset_command)
    if exit_code != 0:
        logging.error(f"重置本地代码失败: {stderr}")
        print(f"重置本地代码失败: {stderr}")
        return False
    
    logging.info(f"成功更新仓库 {repo_dir}")
    print(f"成功更新仓库 {repo_dir}")
    return True

def sync_git_repo_backend(logger=None, new_version_str=None):
    """
    主函数，用于演示如何使用上述功能
    """
    # 定义日志函数
    def log(message):
        if logger:
            logger.write(message)
        else:
            print(message)
    
    # 服务器信息
    server_ip = "47.99.204.97"
    username = "Administrator"  # 假设使用root用户，根据实际情况修改
    password = "Sjw9@0613"
    
    # 固定的GitHub仓库URL
    github_repo = "https://github.com/Pigbowl/BackEndS.git"
    log(f"使用GitHub仓库URL: {github_repo}")
    # 固定的服务器目标目录
    target_dir = "C:\\Users\\Administrator\\Desktop\\darkerback"
    log(f"使用服务器目录: {target_dir}")
    
    # 连接服务器
    ssh_client = connect_remote_server(server_ip, username, password)
    
    if ssh_client:
        try:
            # 检查目标目录是否存在，并且是否为Git仓库
            check_dir_command = f'powershell -Command "Test-Path \"{target_dir}\\.git\""'
            stdout, stderr, exit_code = execute_command(ssh_client, check_dir_command)
            
            if "True" in stdout.strip():
                log(f"检测到目标目录 {target_dir} 已经是一个Git仓库，执行更新操作...")
                success = git_pull(ssh_client, target_dir)
                if success:
                    log("Git仓库更新操作完成！")
                else:
                    log("Git仓库更新操作失败！")
            else:
                # 检查目录是否存在但不是Git仓库
                check_exist_command = f'powershell -Command "Test-Path \"{target_dir}\""'
                stdout, stderr, exit_code = execute_command(ssh_client, check_exist_command)
                
                if "True" in stdout.strip():
                    log(f"目标目录 {target_dir} 已存在但不是Git仓库，先删除再克隆...")
                    # 删除已存在的目录
                    delete_dir_command = f'powershell -Command "Remove-Item -Path \"{target_dir}\" -Recurse -Force"'
                    stdout, stderr, exit_code = execute_command(ssh_client, delete_dir_command)
                    
                # 克隆仓库
                success = git_clone(ssh_client, github_repo, target_dir)
                
                if success:
                    log("Git仓库克隆操作完成！")
                else:
                    log("Git仓库克隆操作失败！")
                
        finally:
            # 关闭SSH连接
            ssh_client.close()
            logging.info("SSH连接已关闭")
            log("SSH连接已关闭")

def sync_git_repo_darkertech(local_dir, logger=None, commit_title=None, commit_desc=None):
    """
    将本地darkertech文件夹的内容推送到GitHub仓库
    :param local_dir: 本地darkertech文件夹路径
    :param logger: 日志记录器，用于记录日志
    :param commit_title: 自定义commit标题（可选）
    :param commit_desc: 自定义commit描述（可选）
    :return: bool - 操作是否成功
    """
    import subprocess
    import os
    from datetime import datetime
    
    # 定义日志函数
    def log(message):
        if logger:
            logger.write(message)
        else:
            print(message)
    
    # 固定的GitHub仓库URL
    github_repo = "https://github.com/Pigbowl/Darker-tech.git"
    log(f"使用GitHub仓库URL: {github_repo}")
    # log(f"使用本地目录: {local_dir}")
    
    # 保存当前工作目录
    original_dir = os.getcwd()
    # log(f"当前工作目录: {original_dir}")
    
    try:
        # 检查本地目录是否存在
        if not os.path.exists(local_dir):
            log(f"错误: 本地目录 {local_dir} 不存在")
            return False
        
        # 切换到本地目录
        os.chdir(local_dir)
        # log(f"切换到目录: {local_dir}")
        
        # 检查是否已经是Git仓库
        if not os.path.exists(".git"):
            log("本地目录不是Git仓库，开始初始化...")
            
            # 初始化Git仓库
            result = subprocess.run(["git", "init"], capture_output=True, text=True, encoding='utf-8', check=True)
            log(f"Git初始化成功")
            
            # 添加远程仓库
            result = subprocess.run(["git", "remote", "add", "origin", github_repo], capture_output=True, text=True, encoding='utf-8', check=True)
            log(f"添加远程仓库成功")
        # else:
        #     log("本地目录已经是Git仓库")
        
        # 检查远程仓库配置
        result = subprocess.run(["git", "remote", "get-url", "origin"], capture_output=True, text=True, encoding='utf-8')
        if result.returncode == 0:
            current_remote = result.stdout.strip()
            log(f"当前远程仓库: {current_remote}")
            if current_remote != github_repo:
                log(f"远程仓库不一致，更新远程仓库URL")
                result = subprocess.run(["git", "remote", "set-url", "origin", github_repo], capture_output=True, text=True, encoding='utf-8', check=True)
                log(f"更新远程仓库URL成功")
            else:
                log(f"远程仓库配置正确")
        else:
            log(f"未配置远程仓库，添加远程仓库")
            result = subprocess.run(["git", "remote", "add", "origin", github_repo], capture_output=True, text=True, encoding='utf-8', check=True)
            log(f"添加远程仓库成功")
        
        # 添加所有文件
        result = subprocess.run(["git", "add", "."], capture_output=True, text=True, encoding='utf-8', check=True)
        log(f"添加所有文件成功")
        
        # 提交更改
        try:
            # 如果提供了自定义commit标题，使用自定义标题和描述
            if commit_title:
                if commit_desc:
                    # 使用多行commit消息
                    commit_msg = f"{commit_title}\n\n{commit_desc}"
                    # 使用echo和管道来创建多行commit消息
                    echo_cmd = f'echo \"{commit_title}\n\n{commit_desc}\" | git commit -F -'
                    result = subprocess.run(echo_cmd, capture_output=True, text=True, encoding='utf-8', shell=True)
                else:
                    # 只有自定义标题
                    commit_msg = commit_title
                    result = subprocess.run(["git", "commit", "-m", commit_msg], capture_output=True, text=True, encoding='utf-8')
            else:
                # 自动生成commit消息
                try:
                    # 尝试获取最新的commit信息
                    last_commit = subprocess.check_output(["git", "log", "--oneline", "-1"], text=True, encoding='utf-8').strip()
                    # 使用当前时间和上一次commit信息
                    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    commit_msg = f'Auto commit - {current_time}'
                except subprocess.CalledProcessError:
                    # 如果是新仓库，没有提交记录，使用Initial commit
                    commit_msg = 'Initial commit'
                result = subprocess.run(["git", "commit", "-m", commit_msg], capture_output=True, text=True, encoding='utf-8')
        except Exception as e:
            log(f"生成commit消息失败: {e}")
            return False
        
        if result.returncode == 0:
            log(f"提交成功: {commit_msg}")
        else:
            # 检查是否没有需要提交的更改
            if "nothing to commit" in result.stderr or "nothing added to commit" in result.stderr:
                log("没有需要提交的更改")
                # 没有需要提交的更改时，不视为失败，继续执行后续操作
            else:
                log(f"提交失败: {result.stderr}")
                return False
        
        # 推送到GitHub仓库
        result = subprocess.run(["git", "push", "origin", "main"], capture_output=True, text=True, encoding='utf-8', check=True)
        log(f"推送成功")
        # log(f"已将 {local_dir} 推送到 {github_repo}")
        return True
    except subprocess.CalledProcessError as e:
        log(f"Git命令执行失败: {e.cmd}")
        log(f"输出: {e.stdout}")
        log(f"错误: {e.stderr}")
        return False
    except Exception as e:
        log(f"操作失败: {e}")
        return False
    finally:
        # 恢复到原来的工作目录
        os.chdir(original_dir)
        # log(f"已恢复到原来的工作目录: {original_dir}")

def git_commit_backend(local_dir, logger=None, commit_title=None, commit_desc=None):
    """
    执行本地BackendS文件夹的git commit操作
    :param local_dir: 本地BackendS文件夹路径
    :param logger: 日志记录器，用于记录日志
    :param commit_title: 自定义commit标题（可选）
    :param commit_desc: 自定义commit描述（可选）
    :return: tuple - (bool: 操作是否成功, str: commit消息或空字符串)
    """
    import subprocess
    import os
    from datetime import datetime
    
    # 定义日志函数
    def log(message):
        if logger:
            logger.write(message)
        else:
            print(message)
    
    # 固定的GitHub仓库URL
    github_repo = "https://github.com/Pigbowl/BackEndS.git"
    
    # 保存当前工作目录
    original_dir = os.getcwd()
    commit_msg = ""
    
    try:
        # 检查本地目录是否存在
        if not os.path.exists(local_dir):
            log(f"错误: 本地目录 {local_dir} 不存在")
            return False, commit_msg
        
        # 切换到本地目录
        os.chdir(local_dir)
        log(f"切换到目录: {local_dir}")
        
        # 检查是否已经是Git仓库
        if not os.path.exists(".git"):
            log("本地目录不是Git仓库，开始初始化...")
            
            # 初始化Git仓库
            result = subprocess.run(["git", "init"], capture_output=True, text=True, encoding='utf-8', check=True)
            log(f"Git初始化成功")
            
            # 添加远程仓库
            result = subprocess.run(["git", "remote", "add", "origin", github_repo], capture_output=True, text=True, encoding='utf-8', check=True)
            log(f"添加远程仓库成功")
        else:
            log("本地目录已经是Git仓库")
        
        # 检查远程仓库配置
        result = subprocess.run(["git", "remote", "get-url", "origin"], capture_output=True, text=True, encoding='utf-8')
        if result.returncode == 0:
            current_remote = result.stdout.strip()
            log(f"当前远程仓库: {current_remote}")
            if current_remote != github_repo:
                log(f"远程仓库不一致，更新远程仓库URL")
                result = subprocess.run(["git", "remote", "set-url", "origin", github_repo], capture_output=True, text=True, encoding='utf-8', check=True)
                log(f"更新远程仓库URL成功")
        else:
            log(f"未配置远程仓库，添加远程仓库")
            result = subprocess.run(["git", "remote", "add", "origin", github_repo], capture_output=True, text=True, encoding='utf-8', check=True)
            log(f"添加远程仓库成功")
        
        # 添加所有文件
        result = subprocess.run(["git", "add", "."], capture_output=True, text=True, encoding='utf-8', check=True)
        log(f"添加所有文件成功")
        
        # 提交更改
        try:
            # 如果提供了自定义commit标题，使用自定义标题和描述
            if commit_title:
                if commit_desc:
                    # 使用多行commit消息
                    commit_msg = f"{commit_title}\n\n{commit_desc}"
                    # 使用echo和管道来创建多行commit消息
                    echo_cmd = f'echo \"{commit_title}\n\n{commit_desc}\" | git commit -F -'
                    result = subprocess.run(echo_cmd, capture_output=True, text=True, encoding='utf-8', shell=True)
                else:
                    # 只有自定义标题
                    commit_str = f'{commit_title}-Official_Release'
                    
                    try:
                        # 尝试获取最新的commit信息，检查是否重复
                        last_commit = subprocess.check_output(["git", "log", "--oneline", "-1"], text=True, encoding='utf-8').strip()
                        commit_hash, *rest = last_commit.split(maxsplit=1)
                        commit_msg_part = ' '.join(rest) if rest else ''
                        if commit_msg_part == commit_str:
                            print("redundant commit message")
                    except subprocess.CalledProcessError:
                        # 新仓库，没有提交记录，继续执行
                        pass
                    
                    commit_msg = commit_str
                    result = subprocess.run(["git", "commit", "-m", commit_msg], capture_output=True, text=True, encoding='utf-8')

            else:
                # 自动生成commit消息
                try:
                    # 尝试获取最新的commit信息
                    last_commit = subprocess.check_output(["git", "log", "--oneline", "-1"], text=True, encoding='utf-8').strip()
                    # 使用当前时间和上一次commit信息
                    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    commit_msg = f'Auto commit - {current_time}'
                except subprocess.CalledProcessError:
                    # 如果是新仓库，没有提交记录，使用Initial commit
                    commit_msg = 'Initial commit'
                result = subprocess.run(["git", "commit", "-m", commit_msg], capture_output=True, text=True, encoding='utf-8')
        except Exception as e:
            log(f"生成commit消息失败: {e}")
            return False, ""
        
        if result.returncode == 0:
            log(f"Commit 提交成功: {commit_msg}")
            return True, commit_msg
        else:
            if "nothing to commit" in result.stderr:
                log("没有需要提交的更改")
                return True, ""  # 没有需要提交的更改时，视为成功，但返回空的commit消息
            else:
                log(f"Commit 提交失败: {result.stderr}")
                return False, ""
    except subprocess.CalledProcessError as e:
        log(f"Git命令执行失败: {e.cmd}")
        log(f"输出: {e.stdout}")
        log(f"错误: {e.stderr}")
        return False, ""
    except Exception as e:
        log(f"操作失败: {e}")
        return False, ""
    finally:
        # 恢复到原来的工作目录
        os.chdir(original_dir)


def git_rollback_commit(local_dir, logger=None, expected_commit_msg=None):
    """
    撤回本地最近的commit，如果commit消息匹配预期
    :param local_dir: 本地仓库路径
    :param logger: 日志记录器，用于记录日志
    :param expected_commit_msg: 预期的commit消息，用于验证是否是要撤回的commit
    :return: bool - 操作是否成功
    """
    import subprocess
    import os
    
    # 定义日志函数
    def log(message):
        if logger:
            logger.write(message)
        else:
            print(message)
    
    # 保存当前工作目录
    original_dir = os.getcwd()
    
    try:
        # 检查本地目录是否存在
        if not os.path.exists(local_dir):
            log(f"错误: 本地目录 {local_dir} 不存在")
            return False
        
        # 切换到本地目录
        os.chdir(local_dir)
        log(f"切换到目录: {local_dir}")
        
        # 获取最近的commit信息
        result = subprocess.run(["git", "log", "--format=%B", "-1"], capture_output=True, text=True, encoding='utf-8')
        if result.returncode != 0:
            log(f"获取最近commit信息失败: {result.stderr}")
            return False
        
        # 提取最近的commit消息
        latest_commit_msg = result.stdout.strip()
        log(f"最近的commit消息: {latest_commit_msg}")
        
        # 验证commit消息是否匹配
        if expected_commit_msg and latest_commit_msg == expected_commit_msg:
            log(f"验证通过，准备撤回commit: {expected_commit_msg}")
            
            # 执行撤回操作 (--soft 保留更改，--hard 不保留更改)
            result = subprocess.run(["git", "reset", "--soft", "HEAD~1"], capture_output=True, text=True, encoding='utf-8')
            if result.returncode == 0:
                log(f"成功撤回commit: {expected_commit_msg}")
                return True
            elif "unknown revision or path not in the working tree" in result.stderr:
                # 处理新仓库只有一个commit的情况
                log(f"这是仓库的第一个commit，无法使用HEAD~1撤回")
                # 尝试使用git reset --soft HEAD^，这对于第一个commit也会失败
                log(f"撤回commit失败: {result.stderr}")
                return False
            else:
                log(f"撤回commit失败: {result.stderr}")
                return False
        elif not expected_commit_msg:
            log(f"未提供预期commit消息，跳过撤回")
            return False
        else:
            log(f"最近的commit消息与预期不符，跳过撤回")
            log(f"预期: {expected_commit_msg}")
            log(f"实际: {latest_commit_msg}")
            return False
    except subprocess.CalledProcessError as e:
        log(f"Git命令执行失败: {e.cmd}")
        log(f"输出: {e.stdout}")
        log(f"错误: {e.stderr}")
        return False
    except Exception as e:
        log(f"操作失败: {e}")
        return False
    finally:
        # 恢复到原来的工作目录
        os.chdir(original_dir)


def git_commit_darkertech(local_dir, logger=None, commit_title=None, commit_desc=None):
    """
    执行本地darkertech文件夹的git commit操作
    :param local_dir: 本地darkertech文件夹路径
    :param logger: 日志记录器，用于记录日志
    :param commit_title: 自定义commit标题（可选）
    :param commit_desc: 自定义commit描述（可选）
    :return: tuple - (bool, str) 操作是否成功，commit消息
    """
    import subprocess
    import os
    from datetime import datetime
    
    # 定义日志函数
    def log(message):
        if logger:
            logger.write(message)
        else:
            print(message)
    
    # 保存当前工作目录
    original_dir = os.getcwd()
    
    try:
        # 检查本地目录是否存在
        if not os.path.exists(local_dir):
            log(f"错误: 本地目录 {local_dir} 不存在")
            return False, ""
        
        # 切换到本地目录
        os.chdir(local_dir)
        
        # 检查是否已经是Git仓库
        if not os.path.exists(".git"):
            log("本地目录不是Git仓库，开始初始化...")
            
            # 初始化Git仓库
            result = subprocess.run(["git", "init"], capture_output=True, text=True, encoding='utf-8', check=True)
            log(f"Git初始化成功")
            
            # 添加远程仓库
            github_repo = "https://github.com/Pigbowl/Darker-tech.git"
            result = subprocess.run(["git", "remote", "add", "origin", github_repo], capture_output=True, text=True, encoding='utf-8', check=True)
            log(f"添加远程仓库成功")
        
        # 添加所有文件
        result = subprocess.run(["git", "add", "."], capture_output=True, text=True, encoding='utf-8')
        log(f"添加所有文件成功")
        
        # 生成commit消息
        commit_msg = ""
        if commit_title:
            if commit_desc:
                # 使用多行commit消息
                commit_msg = f'{commit_title}\n\n{commit_desc}'
                # 使用echo和管道来创建多行commit消息
                echo_cmd = f'echo \"{commit_title}\n\n{commit_desc}\" | git commit -F -'
                result = subprocess.run(echo_cmd, capture_output=True, text=True, encoding='utf-8', shell=True)
            else:
                # 只有自定义标题
                commit_msg = commit_title
                result = subprocess.run(["git", "commit", "-m", commit_msg], capture_output=True, text=True, encoding='utf-8')
        else:
            # 自动生成commit消息
            try:
                # 尝试获取最新的commit信息
                last_commit = subprocess.check_output(["git", "log", "--oneline", "-1"], text=True, encoding='utf-8').strip()
                # 使用当前时间和上一次commit信息
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                commit_msg = f'Auto commit - {current_time}'
            except subprocess.CalledProcessError:
                # 如果是新仓库，没有提交记录，使用Initial commit
                commit_msg = 'Initial commit'
            result = subprocess.run(["git", "commit", "-m", commit_msg], capture_output=True, text=True, encoding='utf-8')
        
        if result.returncode == 0:
            log(f"Commit 提交成功: {commit_msg}")
            return True, commit_msg
        else:
            if "nothing to commit" in result.stderr:
                log("没有需要提交的更改")
                return True, ""  # 没有需要提交的更改时，视为成功，但返回空的commit消息
            else:
                log(f"Commit 提交失败: {result.stderr}")
                return False, ""
    except subprocess.CalledProcessError as e:
        log(f"Git命令执行失败: {e.cmd}")
        log(f"输出: {e.stdout}")
        log(f"错误: {e.stderr}")
        return False, ""
    except Exception as e:
        log(f"操作失败: {e}")
        return False, ""
    finally:
        # 恢复到原来的工作目录
        os.chdir(original_dir)


def git_push_darkertech(local_dir, logger=None):
    """
    执行本地darkertech文件夹的git push操作
    :param local_dir: 本地darkertech文件夹路径
    :param logger: 日志记录器，用于记录日志
    :return: bool - 操作是否成功
    """
    import subprocess
    import os
    
    # 定义日志函数
    def log(message):
        if logger:
            logger.write(message)
        else:
            print(message)
    
    # 保存当前工作目录
    original_dir = os.getcwd()
    
    try:
        # 检查本地目录是否存在
        if not os.path.exists(local_dir):
            log(f"错误: 本地目录 {local_dir} 不存在")
            return False
        
        # 切换到本地目录
        os.chdir(local_dir)
        
        # 固定的GitHub仓库URL
        github_repo = "https://github.com/Pigbowl/Darker-tech.git"
        
        # 推送到GitHub仓库
        log(f"开始推送代码到GitHub仓库: {github_repo}")
        result = subprocess.run(["git", "push", "origin", "main"], capture_output=True, text=True, encoding='utf-8')
        
        if result.returncode == 0:
            log(f"Darker-tech 代码向 Github 推送成功")
            return True
        else:
            log(f"推送失败: {result.stderr}")
            return False
    except subprocess.CalledProcessError as e:
        log(f"Git命令执行失败: {e.cmd}")
        log(f"输出: {e.stdout}")
        log(f"错误: {e.stderr}")
        return False
    except Exception as e:
        log(f"操作失败: {e}")
        return False
    finally:
        # 恢复到原来的工作目录
        os.chdir(original_dir)


def git_push_backend(local_dir, logger=None):
    """
    执行本地BackendS文件夹的git push操作
    :param local_dir: 本地BackendS文件夹路径
    :param logger: 日志记录器，用于记录日志
    :return: bool - 操作是否成功
    """
    import subprocess
    import os
    
    # 定义日志函数
    def log(message):
        if logger:
            logger.write(message)
        else:
            print(message)
    
    # 固定的GitHub仓库URL
    github_repo = "https://github.com/Pigbowl/BackEndS.git"
    
    # 保存当前工作目录
    original_dir = os.getcwd()
    
    try:
        # 检查本地目录是否存在
        if not os.path.exists(local_dir):
            log(f"错误: 本地目录 {local_dir} 不存在")
            return False
        
        # 切换到本地目录
        os.chdir(local_dir)
        log(f"切换到目录: {local_dir}")
        
        # 推送到GitHub仓库
        log(f"开始推送代码到GitHub仓库: {github_repo}")
        result = subprocess.run(["git", "push", "origin", "main"], capture_output=True, text=True, encoding='utf-8')
        
        if result.returncode == 0:
            log(f"BackEndS 代码向 Github 推送成功")
            return True
        else:
            log(f"推送失败: {result.stderr}")
            return False
    except subprocess.CalledProcessError as e:
        log(f"Git命令执行失败: {e.cmd}")
        log(f"输出: {e.stdout}")
        log(f"错误: {e.stderr}")
        return False
    except Exception as e:
        log(f"操作失败: {e}")
        return False
    finally:
        # 恢复到原来的工作目录
        os.chdir(original_dir)


def sync_backend_to_github(local_dir, logger=None, commit_title=None, commit_desc=None):
    """
    将本地BackendS文件夹的内容推送到GitHub仓库（兼容旧接口）
    :param local_dir: 本地BackendS文件夹路径
    :param logger: 日志记录器，用于记录日志
    :param commit_title: 自定义commit标题（可选）
    :param commit_desc: 自定义commit描述（可选）
    :return: bool - 操作是否成功
    """
    # 先执行commit
    commit_result = git_commit_backend(local_dir, logger, commit_title, commit_desc)
    if not commit_result:
        return False
    
    # 再执行push
    push_result = git_push_backend(local_dir, logger)
    return push_result


if __name__ == "__main__":
    sync_git_repo_backend()
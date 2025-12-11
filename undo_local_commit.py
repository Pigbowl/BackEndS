import os
import subprocess


def undo_last_local_commit(repo_path=None, hard=False):
    """
    撤回本地仓库中最后一个未推送的commit
    
    Args:
        repo_path (str, optional): 本地仓库路径，如果不提供则使用当前目录
        hard (bool, optional): 是否使用hard重置，True表示丢弃修改，False表示保留修改（默认）
    
    Returns:
        str: 操作结果信息
    """
    try:
        # 如果提供了仓库路径，切换到该目录
        original_dir = os.getcwd()
        if repo_path:
            if not os.path.exists(repo_path):
                return f"错误: 仓库路径 {repo_path} 不存在"
            os.chdir(repo_path)
        
        # 检查当前目录是否是git仓库
        is_git_repo_cmd = "git rev-parse --is-inside-work-tree"
        is_git_repo_result = subprocess.run(
            is_git_repo_cmd, 
            shell=True, 
            capture_output=True, 
            text=True
        )
        if is_git_repo_result.returncode != 0:
            return f"错误: 当前目录 {os.getcwd()} 不是git仓库"
        
        # 获取当前分支
        branch_cmd = "git rev-parse --abbrev-ref HEAD"
        branch_result = subprocess.run(
            branch_cmd, 
            shell=True, 
            check=True, 
            capture_output=True, 
            text=True
        )
        current_branch = branch_result.stdout.strip()
        
        # 获取最后一个commit信息
        last_commit_cmd = "git show --oneline -s HEAD"
        last_commit_result = subprocess.run(
            last_commit_cmd, 
            shell=True, 
            check=True, 
            capture_output=True, 
            text=True
        )
        last_commit_info = last_commit_result.stdout.strip()
        
        # 检查是否有commit可以撤回
        log_cmd = "git log --oneline"
        log_result = subprocess.run(
            log_cmd, 
            shell=True, 
            check=True, 
            capture_output=True, 
            text=True
        )
        commits = log_result.stdout.strip().split('\n')
        if not commits or commits[0].strip() == '':
            return f"错误: 当前分支 {current_branch} 上没有commit可以撤回"
        
        # 执行reset命令
        reset_mode = "--hard" if hard else "--soft"
        reset_cmd = f"git reset {reset_mode} HEAD~1"
        reset_result = subprocess.run(
            reset_cmd, 
            shell=True, 
            check=True, 
            capture_output=True, 
            text=True
        )
        
        # 获取操作后的仓库状态
        status_cmd = "git status"
        status_result = subprocess.run(
            status_cmd, 
            shell=True, 
            check=True, 
            capture_output=True, 
            text=True
        )
        
        # 构建结果信息
        result = f"成功撤回最后一个commit:\n"
        result += f"  分支: {current_branch}\n"
        result += f"  撤回的commit: {last_commit_info}\n"
        result += f"  重置模式: {reset_mode}\n"
        result += f"  操作结果: {reset_result.stdout.strip()}\n"
        result += f"\n当前仓库状态:\n{status_result.stdout}"
        
        return result
        
    except subprocess.CalledProcessError as e:
        return f"执行git命令时出错: {e.stderr.strip()}\n命令: {e.cmd}"
    except Exception as e:
        return f"发生未知错误: {str(e)}"
    finally:
        # 切换回原始目录
        os.chdir(original_dir)


# 示例用法
if __name__ == "__main__":
    # # 示例1：在当前目录操作，保留修改
    # print("示例1：在当前目录操作，保留修改")
    # result1 = undo_last_local_commit()
    # print(result1)
    # print("\n" + "="*50 + "\n")

    repo_path = "C:\\Users\\宋嘉玮\\OneDrive\\Desktop\\BackEndS"
    print("示例2：指定仓库路径，使用hard重置")
    result2 = undo_last_local_commit(repo_path=repo_path, hard=True)
    print(result2)

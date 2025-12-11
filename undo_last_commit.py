import os
import subprocess
import tempfile
import shutil


def undo_last_unsynced_commit(github_url):
    """
    撤回GitHub仓库中最后一个未同步到远程的commit
    
    Args:
        github_url (str): GitHub仓库的URL，例如 "https://github.com/username/repo.git"
    
    Returns:
        str: 操作结果信息
    """
    # 临时目录，用于克隆或操作仓库
    temp_dir = tempfile.mkdtemp()
    repo_name = github_url.split('/')[-1].replace('.git', '')
    repo_path = os.path.join(temp_dir, repo_name)
    
    try:
        # 步骤1：克隆仓库到临时目录
        print(f"正在克隆仓库到临时目录: {temp_dir}")
        clone_cmd = f"git clone {github_url} {repo_path}"
        subprocess.run(clone_cmd, shell=True, check=True, capture_output=True, text=True)
        
        # 步骤2：切换到仓库目录
        os.chdir(repo_path)
        
        # 步骤3：获取当前分支
        branch_cmd = "git rev-parse --abbrev-ref HEAD"
        branch_result = subprocess.run(branch_cmd, shell=True, check=True, capture_output=True, text=True)
        current_branch = branch_result.stdout.strip()
        print(f"当前分支: {current_branch}")
        
        # 步骤4：获取远程仓库最新信息
        fetch_cmd = "git fetch"
        subprocess.run(fetch_cmd, shell=True, check=True, capture_output=True, text=True)
        
        # 步骤5：比较本地分支和远程分支的差异
        diff_cmd = f"git log origin/{current_branch}..HEAD"
        diff_result = subprocess.run(diff_cmd, shell=True, check=True, capture_output=True, text=True)
        unsynced_commits = diff_result.stdout.strip().split('\ncommit ')
        
        # 过滤掉空字符串
        unsynced_commits = [commit for commit in unsynced_commits if commit.strip()]
        
        if not unsynced_commits:
            return f"在分支 {current_branch} 上没有未同步到远程的commit"
        
        print(f"找到 {len(unsynced_commits)} 个未同步的commit:")
        
        # 步骤6：显示未同步的commit信息
        for i, commit in enumerate(unsynced_commits):
            if commit:
                lines = commit.split('\n')
                if lines:
                    commit_hash = lines[0].strip()
                    # 获取commit信息
                    log_cmd = f"git show --oneline -s {commit_hash}"
                    log_result = subprocess.run(log_cmd, shell=True, check=True, capture_output=True, text=True)
                    print(f"  {i+1}. {log_result.stdout.strip()}")
        
        # 步骤7：确认要撤回最后一个未同步的commit
        last_commit_hash = unsynced_commits[0].split('\n')[0].strip()
        log_cmd = f"git show --oneline -s {last_commit_hash}"
        log_result = subprocess.run(log_cmd, shell=True, check=True, capture_output=True, text=True)
        last_commit_info = log_result.stdout.strip()
        
        print(f"\n要撤回的最后一个未同步commit: {last_commit_info}")
        
        # 步骤8：执行git reset命令撤回commit（--soft表示保留修改，--hard表示丢弃修改）
        reset_cmd = "git reset --soft HEAD~1"
        subprocess.run(reset_cmd, shell=True, check=True, capture_output=True, text=True)
        
        # 步骤9：验证撤回结果
        status_cmd = "git status"
        status_result = subprocess.run(status_cmd, shell=True, check=True, capture_output=True, text=True)
        
        return f"成功撤回最后一个未同步commit: {last_commit_info}\n\n当前仓库状态:\n{status_result.stdout}"
    
    except subprocess.CalledProcessError as e:
        return f"执行git命令时出错: {e.stderr}\n命令: {e.cmd}"
    except Exception as e:
        return f"发生未知错误: {str(e)}"
    finally:
        # 清理临时目录
        os.chdir(temp_dir)  # 确保退出仓库目录
        shutil.rmtree(temp_dir)


# 示例用法
if __name__ == "__main__":
    # 请替换为实际的GitHub仓库URL
    github_url = "https://github.com/Pigbowl/BackEndS.git"
    result = undo_last_unsynced_commit(github_url)
    print(result)

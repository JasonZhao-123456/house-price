import os
import shutil
import fnmatch

def clean_project():
    """清理项目文件以适配Vercel部署"""
    
    print("🧹 清理项目文件...")
    
    # 1. 删除Python缓存文件
    cache_dirs = []
    for root, dirs, files in os.walk('.'):
        for dir_name in dirs:
            if dir_name == '__pycache__':
                cache_dirs.append(os.path.join(root, dir_name))
            elif dir_name in ['.pytest_cache', '.mypy_cache', '.coverage']:
                cache_dirs.append(os.path.join(root, dir_name))
    
    for cache_dir in cache_dirs:
        try:
            shutil.rmtree(cache_dir)
            print(f"🗑️  删除缓存: {cache_dir}")
        except:
            pass
    
    # 2. 删除不必要的文件类型
    patterns_to_remove = [
        '*.pyc', '*.pyo', '*.pyd', '*.so',
        '*.log', '*.tmp', '*.temp',
        '*.egg-info', '*.dist-info',
        '.DS_Store', 'Thumbs.db'
    ]
    
    for pattern in patterns_to_remove:
        for root, dirs, files in os.walk('.'):
            for file in fnmatch.filter(files, pattern):
                try:
                    os.remove(os.path.join(root, file))
                    print(f"🗑️  删除文件: {file}")
                except:
                    pass
    
    # 3. 检查大文件
    print("\n📊 检查大文件 (>1MB):")
    large_files = []
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith(('.py', '.txt', '.md', '.json', '.yml')):
                continue  # 跳过源代码文件
            
            filepath = os.path.join(root, file)
            try:
                size_mb = os.path.getsize(filepath) / 1024 / 1024
                if size_mb > 1:
                    large_files.append((filepath, size_mb))
            except:
                pass
    
    for filepath, size_mb in large_files:
        print(f"⚠️  {filepath}: {size_mb:.1f}MB")
    
    print(f"\n✅ 清理完成！发现 {len(large_files)} 个大文件")
    return len(large_files) == 0

if __name__ == "__main__":
    clean_project()
    
import os
import sys

def get_folder_size(start_path):
    """计算文件夹总大小"""
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # 跳过如果是符号链接
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)
    return total_size / 1024 / 1024  # MB

print("📊 Vercel部署大小分析")
print("=" * 50)

# 检查各文件夹大小
folders_to_check = ['.', '.venv', '__pycache__']
for folder in folders_to_check:
    if os.path.exists(folder):
        size_mb = get_folder_size(folder)
        print(f"{folder:15} {size_mb:8.1f} MB")

# 检查大文件
print("\n🔍 大文件列表 (>0.5MB):")
for root, dirs, files in os.walk('.'):
    for file in files:
        filepath = os.path.join(root, file)
        # 跳过虚拟环境
        if '.venv' in filepath or '__pycache__' in filepath:
            continue
        
        try:
            size_mb = os.path.getsize(filepath) / 1024 / 1024
            if size_mb > 0.5:
                print(f"  {size_mb:6.1f}MB  {filepath}")
        except:
            pass

# 检查Python包大小
print("\n📦 Python包大小估计:")
try:
    import site
    packages_path = site.getsitepackages()[0]
    if os.path.exists(packages_path):
        size_mb = get_folder_size(packages_path)
        print(f"site-packages: {size_mb:.1f} MB")
except:
    pass

print("\n" + "=" * 50)
print("💡 Vercel限制: 未压缩250MB, 压缩后50MB")
print("💡 建议: 检查.venv是否被上传")

# compress_model.py - 使用临时文件名
import joblib
import os
import shutil

print("🔧 压缩模型文件...")

# 1. 加载原始模型
model = joblib.load('house_price_model.pkl')

# 2. 保存到临时文件
temp_file = 'house_price_model_temp.joblib'
compressed_path = 'house_price_model_compressed.joblib'

# 删除可能存在的临时文件
for f in [temp_file, compressed_path]:
    if os.path.exists(f):
        try:
            os.remove(f)
            print(f"🗑️  已删除旧文件: {f}")
        except:
            print(f"⚠️  无法删除: {f}")

# 3. 保存到临时文件
joblib.dump(model, temp_file, compress=('gzip', 9))

# 4. 重命名回原始文件名
try:
    # 先备份原始文件
    if os.path.exists('house_price_model.pkl'):
        os.rename('house_price_model.pkl', 'house_price_model_backup.pkl')
    
    # 重命名临时文件
    os.rename(temp_file, 'house_price_model.pkl')
    
    print("✅ 压缩完成，文件已替换")
    
except Exception as e:
    print(f"❌ 重命名失败: {e}")
    print("💡 手动操作：")
    print(f"  1. 删除 house_price_model.pkl")
    print(f"  2. 将 {temp_file} 重命名为 house_price_model.pkl")
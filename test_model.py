import joblib
import numpy as np
import pandas as pd

# 1. 加载模型
print("🔍 加载模型文件...")
try:
    model = joblib.load('house_price_model.pkl')
    print(f"✅ 模型加载成功！")
    print(f"模型类型: {type(model).__name__}")
    
    # 查看模型参数
    if hasattr(model, 'n_estimators'):
        print(f"树的数量: {model.n_estimators}")
    if hasattr(model, 'feature_importances_'):
        print(f"特征数量: {len(model.feature_importances_)}")
    
except Exception as e:
    print(f"❌ 模型加载失败: {e}")
    exit()

# 2. 准备测试数据
print("\n🧪 准备测试样本...")
# 创建一个样本房屋的特征
test_house = {
    'area': 85.5,
    'rooms': 3,
    'age': 8,
    'floor': 12,
    'has_parking': 1,
    'location_score': 7.5,
    'is_school_district': 0,
    'metro_distance': 350.0
}

# 转换为DataFrame（保持特征顺序！）
columns = list(test_house.keys())
test_df = pd.DataFrame([test_house], columns=columns)

print("测试特征:")
for col, val in test_house.items():
    print(f"  {col:20s}: {val}")

# 3. 进行预测
print("\n🔮 进行预测...")
try:
    prediction = model.predict(test_df)
    predicted_price = prediction[0]
    print(f"🏠 预测房价: {predicted_price:,.2f} 元")
    print(f"            约 {predicted_price/10000:.1f} 万元")
    
    # 置信区间（基于模型的不确定性）
    if hasattr(model, 'estimators_'):
        # 对每棵树单独预测，计算标准差
        tree_predictions = np.array([tree.predict(test_df)[0] for tree in model.estimators_])
        std_dev = tree_predictions.std()
        print(f"📊 预测波动范围: ±{std_dev:,.0f} 元")
        print(f"   95%置信区间: {predicted_price-1.96*std_dev:,.0f} - {predicted_price+1.96*std_dev:,.0f} 元")
        
except Exception as e:
    print(f"❌ 预测失败: {e}")

# 4. 批量预测示例
print("\n📦 批量预测示例（3个样本）...")
batch_houses = [
    [75.0, 2, 15, 8, 0, 6.0, 0, 800.0],   # 老破小
    [120.0, 4, 5, 15, 1, 9.0, 1, 200.0],  # 豪宅
    [95.0, 3, 10, 10, 1, 7.5, 0, 500.0]   # 改善房
]

batch_df = pd.DataFrame(batch_houses, columns=columns)
batch_predictions = model.predict(batch_df)

for i, (features, price) in enumerate(zip(batch_houses, batch_predictions)):
    print(f"样本{i+1}: {price:,.0f}元 (面积{features[0]}㎡, {features[1]}室)")

print("\n🎯 验证完成！模型文件可以用于API部署了。")
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import joblib
import matplotlib.pyplot as plt
import os

# 1. 加载数据
print("📂 加载数据...")
df = pd.read_csv('house_data.csv')
print(f"数据形状: {df.shape} (行×列)")
print(f"特征列: {list(df.columns[:-1])}")
print(f"目标列: {df.columns[-1]}")

# 2. 准备特征和目标变量
X = df.drop('price', axis=1)  # 所有特征
y = df['price']  # 目标变量（房价）

print(f"\n🎯 特征维度: {X.shape}")
print(f"目标变量范围: {y.min():.0f} - {y.max():.0f}")

# 3. 划分训练集和测试集（80%训练，20%测试）
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
print(f"\n📊 数据集划分:")
print(f"训练集: {X_train.shape[0]} 条样本")
print(f"测试集: {X_test.shape[0]} 条样本")

# 4. 训练模型（这里用随机森林，效果稳定）
print("\n🤖 开始训练随机森林模型...")
model = RandomForestRegressor(
    n_estimators=100,  # 100棵树
    max_depth=10,      # 树的最大深度
    random_state=42,
    n_jobs=-1          # 使用所有CPU核心
)

model.fit(X_train, y_train)
print("✅ 模型训练完成!")

# 5. 评估模型
print("\n📈 模型评估:")
# 训练集预测
y_train_pred = model.predict(X_train)
# 测试集预测
y_test_pred = model.predict(X_test)

# 计算指标
train_mae = mean_absolute_error(y_train, y_train_pred)
test_mae = mean_absolute_error(y_test, y_test_pred)
train_r2 = r2_score(y_train, y_train_pred)
test_r2 = r2_score(y_test, y_test_pred)

print(f"训练集 - 平均绝对误差: {train_mae:,.0f} 元")
print(f"测试集 - 平均绝对误差: {test_mae:,.0f} 元")
print(f"训练集 - R²分数: {train_r2:.4f}")
print(f"测试集 - R²分数: {test_r2:.4f}")

# 6. 特征重要性分析
print("\n🔍 特征重要性排名:")
feature_importance = pd.DataFrame({
    'feature': X.columns,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)

for idx, row in feature_importance.iterrows():
    print(f"  {row['feature']:20s}: {row['importance']:.4f}")

# 7. 保存模型
model_filename = 'house_price_model.pkl'
joblib.dump(model, model_filename)
print(f"\n💾 模型已保存为: {model_filename}")
print(f"模型大小: {os.path.getsize(model_filename) / 1024 / 1024:.2f} MB")

# 8. 可视化结果（可选）
def plot_results():
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    # 1. 预测 vs 实际
    axes[0, 0].scatter(y_test, y_test_pred, alpha=0.5)
    axes[0, 0].plot([y.min(), y.max()], [y.min(), y.max()], 'r--', lw=2)
    axes[0, 0].set_xlabel('实际价格 (元)')
    axes[0, 0].set_ylabel('预测价格 (元)')
    axes[0, 0].set_title('预测 vs 实际')
    axes[0, 0].grid(True, alpha=0.3)
    
    # 2. 误差分布
    errors = y_test - y_test_pred
    axes[0, 1].hist(errors, bins=30, edgecolor='black')
    axes[0, 1].axvline(x=0, color='r', linestyle='--')
    axes[0, 1].set_xlabel('预测误差 (元)')
    axes[0, 1].set_ylabel('频次')
    axes[0, 1].set_title('误差分布')
    axes[0, 1].grid(True, alpha=0.3)
    
    # 3. 特征重要性
    axes[1, 0].barh(feature_importance['feature'][:6], 
                    feature_importance['importance'][:6])
    axes[1, 0].set_xlabel('重要性')
    axes[1, 0].set_title('Top 6 重要特征')
    
    # 4. 残差图
    axes[1, 1].scatter(y_test_pred, errors, alpha=0.5)
    axes[1, 1].axhline(y=0, color='r', linestyle='--')
    axes[1, 1].set_xlabel('预测价格 (元)')
    axes[1, 1].set_ylabel('残差 (元)')
    axes[1, 1].set_title('残差图')
    axes[1, 1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('model_performance.png', dpi=150, bbox_inches='tight')
    plt.show()

# 询问是否显示图表
show_plot = input("\n📊 是否显示可视化图表？(y/n): ").lower()
if show_plot == 'y':
    plot_results()
    print("📷 图表已保存为 model_performance.png")

print("\n🎉 模型训练流程完成！")
print(f"下一步: 使用 {model_filename} 创建API服务")
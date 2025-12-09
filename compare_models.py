from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
import xgboost as xgb
import pandas as pd
from sklearn.model_selection import cross_val_score
import numpy as np

# 加载数据
df = pd.read_csv('house_data.csv')
X = df.drop('price', axis=1)
y = df['price']

# 定义要比较的模型
models = {
    '线性回归': LinearRegression(),
    '决策树': DecisionTreeRegressor(max_depth=5, random_state=42),
    '随机森林': RandomForestRegressor(n_estimators=100, random_state=42),
    '梯度提升': GradientBoostingRegressor(n_estimators=100, random_state=42),
    'XGBoost': xgb.XGBRegressor(n_estimators=100, random_state=42)
}

print("🔬 模型比较（5折交叉验证）")
print("=" * 50)

results = []
for name, model in models.items():
    # 使用交叉验证评估
    scores = cross_val_score(model, X, y, cv=5, scoring='r2')
    mae_scores = -cross_val_score(model, X, y, cv=5, scoring='neg_mean_absolute_error')
    
    results.append({
        '模型': name,
        '平均R²': scores.mean(),
        'R²标准差': scores.std(),
        '平均MAE(元)': mae_scores.mean()
    })
    
    print(f"{name:15s}: R² = {scores.mean():.4f} (±{scores.std():.4f}), "
          f"MAE = {mae_scores.mean():,.0f}元")

# 显示最佳模型
results_df = pd.DataFrame(results).sort_values('平均R²', ascending=False)
print(f"\n🏆 最佳模型: {results_df.iloc[0]['模型']} (R² = {results_df.iloc[0]['平均R²']:.4f})")

# 训练并保存最佳模型
best_model_name = results_df.iloc[0]['模型']
best_model = models[best_model_name]
best_model.fit(X, y)

import joblib
joblib.dump(best_model, f'best_model_{best_model_name}.pkl')
print(f"💾 最佳模型已保存为: best_model_{best_model_name}.pkl")
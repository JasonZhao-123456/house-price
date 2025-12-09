import pandas as pd
import numpy as np

# 生成1000条模拟房价数据
np.random.seed(42)
n_samples = 1000

data = {
    'area': np.random.normal(85, 25, n_samples).clip(40, 200),  # 面积(㎡)
    'rooms': np.random.choice([1, 2, 3, 4], n_samples, p=[0.2, 0.4, 0.3, 0.1]),  # 房间数
    'age': np.random.randint(1, 50, n_samples),  # 房龄(年)
    'floor': np.random.randint(1, 30, n_samples),  # 楼层
    'has_parking': np.random.choice([0, 1], n_samples, p=[0.3, 0.7]),  # 车位
    'location_score': np.random.uniform(1, 10, n_samples),  # 区位评分
    'is_school_district': np.random.choice([0, 1], n_samples, p=[0.7, 0.3]),  # 学区
    'metro_distance': np.random.exponential(500, n_samples).clip(100, 3000),  # 地铁距离
}

# 计算房价（模拟真实关系）
df = pd.DataFrame(data)
# 基础价格公式：2万/㎡ × 面积 + 其他因素
base_price = df['area'] * 20000  # 2万/㎡

# 影响因素
price_adjustment = (
    df['rooms'] * 50000 +  # 每多一间房+5万
    -df['age'] * 3000 +    # 每年折旧3000
    df['floor'] * 1000 +   # 每层+1000
    df['has_parking'] * 80000 +  # 有车位+8万
    df['location_score'] * 30000 +  # 区位分×3万
    df['is_school_district'] * 150000 +  # 学区+15万
    -df['metro_distance'] * 20  # 每远1米-20元
)

# 添加随机噪声
noise = np.random.normal(0, 100000, n_samples)  # 10万标准差噪声

df['price'] = base_price + price_adjustment + noise
df['price'] = df['price'].clip(500000, 5000000)  # 限制在50-500万

# 保存到CSV
df.to_csv('house_data.csv', index=False, encoding='utf-8-sig')
print(f"✅ 已生成 {len(df)} 条房价数据，保存为 house_data.csv")
print(f"📊 价格统计：最低{df['price'].min():.0f}元，最高{df['price'].max():.0f}元，平均{df['price'].mean():.0f}元")

# 显示前5行
print("\n📋 数据示例：")
print(df.head())
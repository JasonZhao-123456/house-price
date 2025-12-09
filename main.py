from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
import os

# 初始化FastAPI应用
app = FastAPI(title="房价预测API", version="1.0")

# 定义输入数据格式 - 根据你的模型特征修改！
class HouseFeatures(BaseModel):
    area: float          # 面积（平方米）
    rooms: int           # 房间数
    age: int             # 房龄（年）
    location_score: float # 区位评分（1-10）
    floor: int           # 楼层
    has_parking: int     # 是否有车位（1/0）
    # 添加你的其他特征...

# 加载模型 - 启动时加载一次
try:
    # 注意：Vercel的路径可能需要调整
    model_path = os.path.join(os.path.dirname(__file__), 'house_price_model.pkl')
    model = joblib.load(model_path)
    print("✅ 模型加载成功！")
except Exception as e:
    print(f"❌ 模型加载失败: {e}")
    model = None

# 根路径，用于测试
@app.get("/")
def read_root():
    return {"message": "房价预测API已启动", "status": "active"}

# 健康检查端点
@app.get("/health")
def health_check():
    if model is not None:
        return {"status": "healthy", "model_loaded": True}
    else:
        return {"status": "unhealthy", "model_loaded": False}

# 预测端点
@app.post("/predict")
def predict(features: HouseFeatures):
    if model is None:
        return {"error": "模型未加载", "predicted_price": None}
    
    try:
        # 1. 将输入转换为模型需要的数组格式
        # 注意：特征顺序必须与训练时完全一致！
        input_data = np.array([[
            features.area,
            features.rooms,
            features.age,
            features.location_score,
            features.floor,
            features.has_parking,
            # ... 你的其他特征，顺序要一致
        ]])
        
        # 2. 进行预测
        prediction = model.predict(input_data)
        
        # 3. 返回结果
        return {
            "status": "success",
            "predicted_price": float(round(prediction[0], 2)),
            "input_features": features.dict(),
            "model_type": str(type(model).__name__)
        }
    except Exception as e:
        return {"error": f"预测失败: {str(e)}", "predicted_price": None}

# 批量预测端点（可选）
@app.post("/batch_predict")
def batch_predict(features_list: list[HouseFeatures]):
    # 类似处理多个输入
    pass
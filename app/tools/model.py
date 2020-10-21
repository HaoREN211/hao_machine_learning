# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2020/10/20 11:33
# IDE：PyCharm

import pandas as pd
from app.models.data_description import DataFieldDescription
from app import db
from app.forms.model import Model
from sklearn.model_selection import KFold
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# 根据模型id获取模型的名字
def get_model_name_by_model_id(model_id):
    models = Model()
    model_names = list(filter(lambda x: x[0] == model_id, models.list_models))
    if model_names:
        return model_names[0][1]
    return None

# 根据提供的field_id提取相关的数据
def get_data_frame(list_fields_id, scene_id=1):
    result_data_frame = pd.DataFrame()

    # 找到场景对应的字段列表
    database_data = DataFieldDescription.query.filter_by(scene_id=scene_id).all()

    # 根据选择的特征id列表，找到对应的特征字段名列表
    list_fields_name = [x.field_name for x in database_data if x.id in list_fields_id]
    list_fields_name.append("label")
    list_description = [x.field_description for x in database_data if x.id in list_fields_id]

    # 根据字段名列表，从原始数据集中提取选中字段名列表的子数据集
    list_value = list(db.session.execute("SELECT " + ",".join(list_fields_name) + " FROM data_fraud_phone"))

    # 将数据整理好，放进数据集中
    for index, value in enumerate(list_fields_name):
        result_data_frame[value] = [x[index] for x in list_value]

    return result_data_frame, ",".join(list_description)

# 加工模型需要的数据集，并根据模型的id选择对应的模型进行训练
def machine_learning_model(field_selected, model_id, scene_id):
    # 根据输入的特征id列表，获取对应的子数据集
    list_filed_id = [int(x) for x in str(field_selected).split("-")[:-1]]
    data, columns = get_data_frame(list_filed_id, int(scene_id))

    # 根据模型id找到模型的名称
    model_name = get_model_name_by_model_id(model_id)

    result = {}
    if model_name == "决策树":
        result = model_decision_tree(data)
    result["columns"] = columns
    return result

# 决策树模型
def model_decision_tree(data, n_split=3, label="label"):
    # 提取训练数据和标签
    X = data.drop(columns=[label]).copy()

    # 多折交叉验证
    kf = KFold(n_splits=n_split)
    predict_result = pd.DataFrame(columns=["y", "y_predict"])
    for train_index, test_index in kf.split(data):
        # 拆分训练集和测试集
        train_X, train_y = X.loc[train_index, :], list(data.loc[train_index, :][label].values)
        test_X, test_y = X.loc[test_index, :], list(data.loc[test_index, :][label].values)

        # 使用训练集训练模型，然后使用测试集验证模型的效果
        dt_model = DecisionTreeClassifier()
        dt_model.fit(train_X, train_y)
        predict_result = predict_result.append(pd.DataFrame({
            "y": test_y,
            "y_predict": list(dt_model.predict(test_X))
        }))
    predict_result.reset_index(drop=True, inplace=True)

    return get_predict_result(list(predict_result["y"].values), list(predict_result["y_predict"].values))

# 根据y的真实值和预测值，验证模型的好坏程度
def get_predict_result(y_true, y_predict):
    return {"accuracy_score": round(accuracy_score(y_true, y_predict), 3),
            "precision_score": round(precision_score(y_true, y_predict), 3),
            "recall_score": round(recall_score(y_true, y_predict), 3),
            "f1_score": round(f1_score(y_true, y_predict), 3)}

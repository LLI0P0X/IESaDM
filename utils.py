import numpy as np
from sklearn.linear_model import LinearRegression
import xgboost as xgb


def clcNumEP(numP: float, numZ: float, numI: float, numVP: float) -> float:
    return numP + numZ + numI - numVP


def clcAPK(numP: float, numVP: float, numD: float, numEP: float) -> float:
    return numP / numVP > numD and numEP > 0


def predictP(listP: list[float]) -> list[float]:
    model = LinearRegression()
    x = np.asarray([range(2017, 2023)]).transpose()
    y = np.asarray([listP]).transpose()
    model.fit(x, y)
    return model.predict([[2023], [2024]])


def predict_next_element_xgboost(data, window_size=3):
    """
    Функция для предсказания следующего элемента списка с использованием XGBoost.

    :param data: Список значений.
    :param window_size: Количество предыдущих значений, используемых для предсказания.
    :return: Прогнозируемое значение следующего элемента.
    """
    # Создаем признаки (предыдущие значения)
    features = []
    target = []
    for i in range(window_size, len(data)):
        features.append(data[i - window_size:i])
        target.append(data[i])

    features = np.array(features)
    target = np.array(target)

    # Создаем модель XGBoost
    model = xgb.XGBRegressor(n_estimators=100, learning_rate=0.1, max_depth=3)

    # Обучаем модель
    model.fit(features, target)

    # Прогнозируем следующее значение
    next_feature = np.array(data[-window_size:]).reshape(1, -1)
    next_element = model.predict(next_feature)

    return next_element[0]

def predict_next_element_linear(data):
    """
    Функция для предсказания следующего элемента списка с использованием линейной регрессии.

    :param data: Список значений.
    :return: Прогнозируемое значение следующего элемента.
    """
    # Создаем признаки (индексы элементов)
    indices = np.arange(len(data)).reshape(-1, 1)

    # Создаем модель линейной регрессии
    model = LinearRegression()

    # Обучаем модель
    model.fit(indices, data)

    # Прогнозируем следующее значение
    next_index = np.array([[len(data)]])
    next_element = model.predict(next_index)

    return round(float(next_element[0]), 3)

if __name__ == '__main__':
    numEP = clcNumEP(5.9, 430, 430, 5.1)
    print(predict_next_element_linear([1, 2, 3, 4, 5, 6]))

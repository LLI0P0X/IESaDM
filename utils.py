import numpy as np
from sklearn.linear_model import LinearRegression


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




if __name__ == '__main__':
    numEP = clcNumEP(5.9, 430, 430, 5.1)
    print(predictP([6273, 7264, 5796, 5931, 6037, 6037]))

import numpy as np

class Lqr:
    def __init__(self, max_velocity):
        self.max_velocity = max_velocity
        self.n = 75
        self.A = self.getA()
        self.R = self.getR()
        self.q = self.getQ()
        self.B = None

    def getA(self):
        return np.array([[1.0, 0, 0],
                         [0, 1.0, 0],
                         [0, 0, 1.0]])

    def getR(self):
        return np.array([[0.01, 0],
                         [0, 0.01]])

    def getQ(self):
        return np.array([[0.639, 0, 0],
                         [0, 1.0, 0],
                         [0, 0, 1.0]])

    def getB(self, yaw, delta_t):
        return np.array([[np.cos(yaw) * delta_t, 0],
                        [np.sin(yaw) * delta_t, 0],
                        [0, delta_t]])


    def lqr(self, setpoint, measured, dt):
        self.B = self.getB(measured[2], dt)

        error = setpoint - measured
        print(error)
        p = [None] * (self.n + 1)

        qf = self.q
        p[self.n] = qf

        for i in range(self.n, 0, -1):
            p[i - 1] = self.q + self.A.T @ p[i] @ self.A - (self.A.T @ p[i] @ self.B) @ np.linalg.pinv(
                self.R + self.B.T @ p[i] @ self.B) @ (self.B.T @ p[i] @ self.A)

        k = [None] * self.n
        u = [None] * self.n

        for i in range(self.n):
            k[i] = -np.linalg.pinv(self.R + self.B.T @ p[i + 1] @ self.B) @ self.B.T @ p[i + 1] @ self.A
            u[i] = k[i] @ error

        u_star = u[self.n - 1]
        return u_star
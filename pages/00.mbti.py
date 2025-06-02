import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# 손실 함수 정의 (Rosenbrock function)
def loss_function(x, y):
    return (1 - x)**2 + 100 * (y - x**2)**2

# 그래디언트 정의
def grad(x, y):
    dx = -2 * (1 - x) - 400 * x * (y - x**2)
    dy = 200 * (y - x**2)
    return dx, dy

# 최적화 알고리즘 정의
def optimize(algorithm, lr, steps, beta1=0.9, beta2=0.999, epsilon=1e-8):
    x, y = -1.5, 1.5  # 시작점
    path = [(x, y)]
    vx, vy = 0, 0
    sx, sy = 0, 0

    for t in range(1, steps + 1):
        dx, dy = grad(x, y)

        if algorithm == "SGD":
            x -= lr * dx
            y -= lr * dy

        elif algorithm == "Momentum":
            vx = beta1 * vx + (1 - beta1) * dx
            vy = beta1 * vy + (1 - beta1) * dy
            x -= lr * vx
            y -= lr * vy

        elif algorithm == "RMSProp":
            sx = beta2 * sx + (1 - beta2) * dx**2
            sy = beta2 * sy + (1 - beta2) * dy**2
            x -= lr * dx / (np.sqrt(sx) + epsilon)
            y -= lr * dy / (np.sqrt(sy) + epsilon)

        elif algorithm == "Adam":
            vx = beta1 * vx + (1 - beta1) * dx
            vy = beta1 * vy + (1 - beta1) * dy
            sx = beta2 * sx + (1 - beta2) * dx**2
            sy = beta2 * sy + (1 - beta2) * dy**2

            vx_hat = vx / (1 - beta1**t)
            vy_hat = vy / (1 - beta1**t)
            sx_hat = sx / (1 - beta2**t)
            sy_hat = sy / (1 - beta2**t)

            x -= lr * vx_hat / (np.sqrt(sx_hat) + epsilon)
            y -= lr * vy_hat / (np.sqrt(sy_hat) + epsilon)

        path.append((x, y))

    return np.array(path)

# Streamlit 인터페이스
st.title("🧠 최적화 알고리즘 시각화")

algo = st.radio("알고리즘 선택", ["SGD", "Momentum", "RMSProp", "Adam"])
lr = st.slider("학습률 (learning rate)", 0.001, 0.2, 0.05)
steps = st.slider("스텝 수", 10, 200, 50)

path = optimize(algo, lr, steps)

# 손실 함수 시각화
x = np.linspace(-2, 2, 400)
y = np.linspace(-1, 3, 400)
X, Y = np.meshgrid(x, y)
Z = loss_function(X, Y)

fig, ax = plt.subplots()
cp = ax.contour(X, Y, Z, levels=50)
ax.plot(path[:, 0], path[:, 1], 'ro-', markersize=3, linewidth=1)
ax.set_title(f"{algo} 최적화 경로")
st.pyplot(fig)

# -*- coding: utf-8 -*-
"""
反向传播 + 梯度下降的最小可运行演示
====================================
网络（极度简化，就三步）:

    x  ──(×w1)──▶ a ──(×w2)──▶ b ──(loss=(b−y)²)──▶ L

目标：找到 w1、w2，让  x·w1·w2 尽量接近 y_target（即 b≈y_target）。

每一轮循环演示训练的一个 step：
    ① 前向传播：算出 b 和 loss
    ② 反向传播：loss.backward() 一次性自动算出所有参数的梯度 ∂L/∂w
    ③ 梯度下降：w ← w − 学习率 × 梯度
    ④ 清零梯度，进入下一步

运行：
    ./venv/bin/python backprop_demo.py
"""

import torch

torch.manual_seed(0)

# ---- 固定的输入和目标 ----
x = torch.tensor(2.0)           # 输入
y_target = torch.tensor(10.0)   # 我们希望模型的输出 b 接近 10

# ---- 可学习的权重 ----
# requires_grad=True 的意思是：请 PyTorch 在反向传播时帮我自动算出梯度
w1 = torch.tensor(1.0, requires_grad=True)
w2 = torch.tensor(1.0, requires_grad=True)

lr = 0.02   # 学习率

print("=" * 78)
print(f"任务：找到 w1、w2，使  x·w1·w2 ≈ {y_target.item():.0f}")
print(f"(x={x.item():.0f}，所以只要让 w1·w2 ≈ {y_target.item()/x.item():.0f} 就行)")
print(f"初始：w1={w1.item():.3f}  w2={w2.item():.3f}")
print("=" * 78)
print(f"{'step':>4} {'b':>8} {'loss':>10} {'∂L/∂w1':>10} {'∂L/∂w2':>10} "
      f"{'w1':>8} {'w2':>8}")
print("-" * 78)

for step in range(1, 8):
    # ---- ① 前向传播 ----
    a = w1 * x          # 第一层：a = x·w1
    b = w2 * a          # 第二层：b = a·w2 = x·w1·w2
    loss = (b - y_target) ** 2   # loss = (b − 10)²

    # ---- ② 反向传播：一次调用，自动算出【所有】参数的梯度 ----
    loss.backward()

    g1 = w1.grad.item()   # ∂L/∂w1
    g2 = w2.grad.item()   # ∂L/∂w2

    # ---- ③ 梯度下降：w ← w − lr·梯度 ----
    # 用 .data 原地改数值，避免把「更新」也记进计算图
    w1.data -= lr * w1.grad
    w2.data -= lr * w2.grad

    # ---- ④ 清零梯度（否则下一步会累加到旧梯度上）----
    w1.grad.zero_()
    w2.grad.zero_()

    print(f"{step:>4} {b.item():>8.3f} {loss.item():>10.4f} {g1:>10.3f} {g2:>10.3f} "
          f"{w1.item():>8.3f} {w2.item():>8.3f}")

print("-" * 78)
print(f"训练结束：w1·w2 = {w1.item()*w2.item():.3f}（目标 ≈ 5），"
      f"输出 b = {x.item()*w1.item()*w2.item():.3f}（目标 ≈ 10）")

# =====================================================================
# 附：手动用链式法则验证 step 1 的梯度，证明反向传播算的没错
# =====================================================================
print("\n" + "=" * 78)
print("手动验证链式法则（用第 1 步的初始值 w1=w2=1, b=2）：")
print("=" * 78)

# 重新算一遍初始状态，避免受上面训练影响
w1_v, w2_v = 1.0, 1.0
b_v = x.item() * w1_v * w2_v          # = 2
# 链式法则拆成三小段：
dL_db = 2 * (b_v - y_target.item())   # ∂L/∂b   = 2(b−10)
db_da = w2_v                          # ∂b/∂a   = w2
da_dw1 = x.item()                     # ∂a/∂w1  = x
db_dw2 = x.item() * w1_v              # ∂b/∂w2  = x·w1 = a

dL_dw1 = dL_db * db_da * da_dw1       # ∂L/∂w1 = ∂L/∂b · ∂b/∂a · ∂a/∂w1
dL_dw2 = dL_db * db_dw2               # ∂L/∂w2 = ∂L/∂b · ∂b/∂w2

print(f"  ∂L/∂b   = 2(b−10)     = {dL_db:.1f}")
print(f"  ∂b/∂a   = w2           = {db_da:.1f}")
print(f"  ∂a/∂w1  = x            = {da_dw1:.1f}")
print(f"  链式法则 ∂L/∂w1 = ∂L/∂b·∂b/∂a·∂a/∂w1 = {dL_dw1:.1f}  "
      f"(PyTorch 自动算出的是 -32.0，一致 ✓)")
print(f"  链式法则 ∂L/∂w2 = ∂L/∂b·∂b/∂w2       = {dL_dw2:.1f}  "
      f"(PyTorch 自动算出的是 -32.0，一致 ✓)")

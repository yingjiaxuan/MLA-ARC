import matplotlib.pyplot as plt
import numpy as np
import os

# ==========================================
# 1. 全局配置 (在此处修改颜色、字体和参数)
# ==========================================

# 样式设置
plt.rcParams['font.family'] = 'sans-serif'  # 论文常用无衬线字体 (Arial/Helvetica风格)
plt.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# 颜色定义 (推荐使用专业配色)
COLOR_DECAY = '#D9534F'      # 衰减红 (MemoryBank)
COLOR_PROTECT = '#5CB85C'    # 保护绿 (MLA-ARC)
COLOR_THRESHOLD = '#777777'  # 阈值灰
COLOR_ZONE = '#F0F0F0'       # 遗忘区背景色
COLOR_TEXT = '#333333'       # 主要文字色

# 核心参数
Y_LIMIT = (0, 1.15)          # Y轴范围
THRESHOLD_VAL = 0.3          # 遗忘阈值 (0.3)
DAYS = 100                   # 模拟总天数
T1_DAY = 90                  # T1 发生的时间点 (3个月后)

# ==========================================
# 2. 数据生成
# ==========================================
t = np.linspace(0, DAYS, 500)

# 模型 A: 标准艾宾浩斯衰减 (MemoryBank)
# S = e^(-t/S0), S0=25
strength_mb = np.exp(-t / 25)

# 模型 B: 你的方法 (MLA-ARC)
# 领域知识被锁定，几乎不衰减 (模拟极慢的线性衰减或常数)
strength_mla = 0.98 - (t * 0.0005) 

# ==========================================
# 3. 绘图逻辑
# ==========================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5), dpi=300, sharey=True)

# --- 子图 1: Standard Approach (MemoryBank) ---
# 绘制曲线
ax1.plot(t, strength_mb, color=COLOR_DECAY, linewidth=3, label='Memory Strength')
# 绘制阈值线
ax1.axhline(y=THRESHOLD_VAL, color=COLOR_THRESHOLD, linestyle='--', linewidth=1.5, alpha=0.7)
# 填充遗忘区域
ax1.fill_between(t, 0, THRESHOLD_VAL, color=COLOR_ZONE, alpha=0.5, label='Forgetting Zone')

# 标题与坐标轴
ax1.set_title('(A) MemoryBank (Baseline)', fontsize=14, fontweight='bold', pad=15)
ax1.set_xlabel('Time (Days)', fontsize=12)
ax1.set_ylabel('Memory Strength ($S$)', fontsize=12)
ax1.set_ylim(Y_LIMIT)
ax1.set_xlim(0, DAYS)

# 标注关键点 T0
ax1.scatter([0], [1], color='black', s=50, zorder=5)
ax1.text(3, 1.02, '$T_0$: Initial Query\n"National Pension"', fontsize=10, color=COLOR_TEXT)

# 标注关键点 T1 (失败)
s_t1_mb = strength_mb[np.searchsorted(t, T1_DAY)]
ax1.scatter([T1_DAY], [s_t1_mb], color=COLOR_DECAY, s=50, zorder=5)
ax1.annotate(f'$T_1$: Retrieval Failed', 
             xy=(T1_DAY, s_t1_mb), xytext=(T1_DAY-40, s_t1_mb+0.25),
             arrowprops=dict(facecolor='black', arrowstyle='->', connectionstyle="arc3,rad=.2"),
             fontsize=10, color='red')

# --- 子图 2: MLA-ARC (Ours) ---
# 绘制曲线
ax2.plot(t, strength_mla, color=COLOR_PROTECT, linewidth=3, label='Protected Strength')
# 绘制阈值线
ax2.axhline(y=THRESHOLD_VAL, color=COLOR_THRESHOLD, linestyle='--', linewidth=1.5, alpha=0.7)
# 填充遗忘区域 (虽然没掉下去，但保留背景作为参考)
ax2.fill_between(t, 0, THRESHOLD_VAL, color=COLOR_ZONE, alpha=0.5)

# 标题与坐标轴
ax2.set_title('(B) MLA-ARC (Ours)', fontsize=14, fontweight='bold', pad=15)
ax2.set_xlabel('Time (Days)', fontsize=12)
ax2.set_xlim(0, DAYS)

# 标注关键点 T0
ax2.scatter([0], [0.98], color='black', s=50, zorder=5)
ax2.text(3, 1.02, '$T_0$: Stored as STM and\ngradually transforming into LTM', fontsize=10, color=COLOR_TEXT)

# 标注关键点 T1 (成功)
s_t1_mla = strength_mla[np.searchsorted(t, T1_DAY)]
ax2.scatter([T1_DAY], [s_t1_mla], color=COLOR_PROTECT, s=50, zorder=5)
ax2.annotate(f'$T_1$: Retrieval Successful\n', 
             xy=(T1_DAY, s_t1_mla), xytext=(T1_DAY-50, 0.6),
             arrowprops=dict(facecolor='black', arrowstyle='->', connectionstyle="arc3,rad=-.2"),
             fontsize=10, color='green')

# 标注“锁定机制”
ax2.text(40, 0.82, 'Memory Evolution\nMechanism', color=COLOR_PROTECT, fontsize=11, fontweight='bold', ha='center')

# ==========================================
# 4. 布局调整与保存
# ==========================================
# 添加总标题
fig.suptitle('Comparison of Memory Behaviors (Concept Map)', fontsize=16, fontweight='bold')

# 调整布局以留出标题空间 (rect=[left, bottom, right, top])
plt.tight_layout(rect=[0, 0, 1, 0.92])

# 获取脚本所在目录
script_dir = os.path.dirname(os.path.abspath(__file__))
save_path_pdf = os.path.join(script_dir, 'figure_2_motivation.pdf')
save_path_png = os.path.join(script_dir, 'figure_2_motivation.png')

# 保存为 PDF (矢量图，适合插入 LaTeX) 和 PNG
plt.savefig(save_path_pdf, format='pdf', bbox_inches='tight')
plt.savefig(save_path_png, format='png', dpi=300, bbox_inches='tight')

print(f"图像生成完毕！已保存至:\n{save_path_pdf}\n{save_path_png}")
plt.show()
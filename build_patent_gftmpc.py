import os
import sys

os.environ.setdefault("MPLCONFIGDIR", os.path.join(os.getcwd(), ".matplotlib"))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


SKILL_SCRIPTS = r"D:\ProgramFiles\CodeTool\skills\claude-skill-patent-writing-chinese-main\scripts"
if SKILL_SCRIPTS not in sys.path:
    sys.path.insert(0, SKILL_SCRIPTS)

from patent_helpers import PatentDoc, mr, m_sub, m_frac, imath, wrap
from figure_helpers import dashed_rect, para, rect, vline, hline, arrow_to


TITLE = "一种基于GFTMPC的柔性钻孔控制方法"
OUT_DOCX = f"{TITLE}.docx"
ASSET_DIR = f"{TITLE}_assets"


def ensure_assets_dir():
    os.makedirs(ASSET_DIR, exist_ok=True)
    return ASSET_DIR


def fig_system_overview():
    path = os.path.join(ASSET_DIR, "fig1_system_overview.png")
    fig, ax = plt.subplots(figsize=(12.5, 7.2))
    ax.set_xlim(0, 12.5)
    ax.set_ylim(0, 7.2)
    ax.axis("off")

    dashed_rect(ax, 0.35, 0.35, 11.8, 6.5, "基于GFTMPC的柔性钻孔控制系统", fontsize=15)

    hole_angle = para(ax, 1.8, 5.8, 2.2, 0.6, "钻孔角度", fontsize=13)
    hist_data = para(ax, 1.8, 4.5, 2.5, 0.7, "历史进给速度\n历史进给扭矩", fontsize=13)
    ref_lib = rect(ax, 4.4, 5.8, 2.4, 0.7, "参考扭矩库", fontsize=13, bold=True)
    gftm = rect(ax, 4.4, 4.4, 2.7, 0.8, "GFTM进给扭矩\n预测模型", fontsize=13, bold=True)
    optimizer = rect(ax, 7.4, 5.0, 2.8, 1.0, "MPC滚动优化器", fontsize=13, bold=True)
    controller = rect(ax, 10.1, 5.0, 2.2, 0.8, "进给速度控制", fontsize=13, bold=True)
    plant = rect(ax, 10.1, 2.6, 2.6, 1.0, "柔性钻孔执行对象\n末端执行器+工件", fontsize=13, bold=True)
    torque_out = para(ax, 7.4, 2.1, 2.5, 0.7, "实时进给扭矩", fontsize=13)
    speed_out = para(ax, 7.4, 0.95, 2.5, 0.7, "实时进给速度", fontsize=13)

    arrow_to(ax, hole_angle["R"], hole_angle["cy"], ref_lib["L"], ref_lib["cy"])
    arrow_to(ax, hole_angle["R"], hole_angle["cy"], gftm["L"], gftm["T"] - 0.12)
    arrow_to(ax, hist_data["R"], hist_data["cy"], gftm["L"], gftm["cy"])
    arrow_to(ax, ref_lib["R"], ref_lib["cy"], optimizer["L"], optimizer["T"] - 0.15)
    arrow_to(ax, gftm["R"], gftm["cy"], optimizer["L"], optimizer["B"] + 0.15)
    arrow_to(ax, optimizer["R"], optimizer["cy"], controller["L"], controller["cy"])
    vline(ax, controller["cx"], controller["B"], 3.35)
    hline(ax, controller["cx"], plant["cx"], 3.35)
    arrow_to(ax, plant["cx"], 3.35, plant["cx"], plant["T"])

    arrow_to(ax, plant["L"], plant["cy"], torque_out["R"], torque_out["cy"])
    arrow_to(ax, plant["L"], plant["B"] + 0.15, speed_out["R"], speed_out["cy"])
    vline(ax, torque_out["cx"], torque_out["T"], 3.5)
    hline(ax, torque_out["cx"], gftm["cx"], 3.5)
    arrow_to(ax, gftm["cx"], 3.5, gftm["cx"], gftm["B"])

    vline(ax, speed_out["cx"], speed_out["T"], 1.45)
    hline(ax, speed_out["cx"], hist_data["cx"], 1.45)
    arrow_to(ax, hist_data["cx"], 1.45, hist_data["cx"], hist_data["B"])

    plt.tight_layout(pad=0.2)
    plt.savefig(path, dpi=220, bbox_inches="tight", facecolor="white")
    plt.close()
    return path


def fig_method_flow():
    path = os.path.join(ASSET_DIR, "fig2_method_flow.png")
    fig, ax = plt.subplots(figsize=(10.8, 8.6))
    ax.set_xlim(0, 10.8)
    ax.set_ylim(0, 8.6)
    ax.axis("off")

    dashed_rect(ax, 0.4, 0.35, 10.0, 7.8, "柔性钻孔控制方法流程", fontsize=15)

    s10 = rect(ax, 5.4, 7.2, 6.2, 0.7, "S10 采集钻孔角度、进给速度与进给扭矩数据", fontsize=13, bold=True)
    s20 = rect(ax, 5.4, 6.0, 6.2, 0.7, "S20 预处理数据并构建多角度参考扭矩库", fontsize=13, bold=True)
    s30 = rect(ax, 5.4, 4.8, 6.2, 0.7, "S30 基于GRU建立GFTM进给扭矩预测模型", fontsize=13, bold=True)
    s40 = rect(ax, 5.4, 3.6, 6.2, 0.7, "S40 以预测扭矩与参考扭矩为输入执行MPC滚动优化", fontsize=13, bold=True)
    s50 = rect(ax, 5.4, 2.4, 6.2, 0.7, "S50 输出优化进给速度并作用于加速段和稳定段", fontsize=13, bold=True)
    s60 = rect(ax, 5.4, 1.2, 6.2, 0.7, "S60 闭环修正进给速度，抑制扭矩突增与断刀风险", fontsize=13, bold=True)

    for upper, lower in [(s10, s20), (s20, s30), (s30, s40), (s40, s50), (s50, s60)]:
        arrow_to(ax, upper["cx"], upper["B"], lower["cx"], lower["T"])

    plt.tight_layout(pad=0.2)
    plt.savefig(path, dpi=220, bbox_inches="tight", facecolor="white")
    plt.close()
    return path


def build_doc(fig1, fig2):
    doc = PatentDoc()

    s_theta = imath(m_sub(mr("theta"), mr("d")))
    s_tauf = imath(m_sub(mr("tau"), mr("f")))
    s_vf = imath(m_sub(mr("v"), mr("f")))
    s_tauref = imath(m_sub(mr("tau"), mr("ref")))
    s_tauk1 = imath(m_sub(mr("tau"), mr("k+1")))
    s_vk = imath(m_sub(mr("v"), mr("k")))
    s_j = imath(mr("J"))

    eq_predict = wrap(
        m_sub(mr("tau"), mr("k+1"))
        + mr("=")
        + mr("GFTM")
        + mr("(")
        + m_sub(mr("theta"), mr("d"))
        + mr(",")
        + m_sub(mr("v"), mr("k"))
        + mr(",")
        + m_sub(mr("tau"), mr("k"))
        + mr(")")
    )
    eq_objective = wrap(
        mr("J")
        + mr("=")
        + m_frac(
            mr("1"),
            mr("1")
        )
        + m_sub(mr("w"), mr("1"))
        + mr("(")
        + m_sub(mr("tau"), mr("pred"))
        + mr("-")
        + m_sub(mr("tau"), mr("ref"))
        + mr(")")
        + mr("^")
        + mr("2")
        + mr("+")
        + m_sub(mr("w"), mr("2"))
        + mr("(")
        + m_sub(mr("Delta v"), mr("f"))
        + mr(")")
        + mr("^")
        + mr("2")
    )

    doc.title(TITLE)

    doc.H("技术领域")
    doc.P("本发明属于轮胎模具自动钻孔与智能控制技术领域，具体涉及一种面向小直径深孔、多钻孔角度工况的基于GFTMPC的柔性钻孔控制方法。")

    doc.H("背景技术")
    doc.P("轮胎模具排气孔加工具有孔径小、深径比大、数量多以及钻孔方向随模具曲面法向变化的特点。传统人工钻孔、专用钻孔设备及数控机床方法难以同时兼顾加工柔性、加工稳定性与加工成本，在多角度深孔加工场景中容易出现断刀、效率低和一致性差等问题。")
    doc.P("现有钻孔控制方式大多采用固定进给参数或基于经验的分段调节策略，难以描述钻孔过程中的非线性、强耦合和时变特性。随着钻孔深度增加，切屑排出阻力、孔壁摩擦以及设备姿态变化会导致进给扭矩呈现动态波动并持续抬升，从而增加断刀风险。")
    doc.P("已有PID控制、滑模控制和自适应控制等方法在钻孔过程控制中存在模型依赖强、参数整定复杂或抗扰能力不足等问题；单纯依赖神经网络预测又难以直接满足约束处理和实时优化要求，因此仍需要一种能够适应多角度工况并兼顾预测能力与约束控制能力的柔性钻孔控制方法。")

    doc.H("发明内容")
    doc.P("本发明的目的在于提供一种基于GFTMPC的柔性钻孔控制方法，通过构建面向钻孔过程的进给扭矩预测模型GFTM，并将其嵌入模型预测控制框架中，对钻孔进给速度进行滚动优化，从而在不同钻孔角度及不同干扰条件下抑制进给扭矩突增，提升深孔钻削稳定性并降低断刀概率。")
    doc.P("为实现上述目的，本发明采用如下技术方案：")
    doc.P("步骤一：采集钻孔过程中的钻孔角度、进给速度和进给扭矩数据，对数据进行滤波预处理，并按照单孔钻削周期建立钻孔过程数据集。", bold=True)
    doc.P("步骤二：基于不同钻孔角度下的历史钻孔数据，提取加速钻孔阶段和稳定钻孔阶段的进给扭矩变化规律，构建多角度参考扭矩库。", bold=True)
    doc.P("步骤三：以钻孔角度、历史进给速度和历史进给扭矩为输入，构建基于GRU神经网络的进给扭矩预测模型GFTM，用于预测下一控制时刻的进给扭矩。", bold=True)
    doc.P("步骤四：将参考扭矩、预测扭矩、进给速度约束和进给速度增量约束引入模型预测控制器，建立以扭矩跟踪误差和控制增量为目标的滚动优化问题。", bold=True)
    doc.P("步骤五：在钻孔执行过程中实时输出优化后的进给速度，并作用于钻孔加速阶段和稳定钻孔阶段，形成进给速度闭环调节。", bold=True)
    doc.P("步骤六：当外部干扰、切屑堵塞趋势或姿态变化导致进给扭矩偏离参考轨迹时，控制器依据预测结果主动调整进给速度，使进给扭矩在预定时间内回归参考轨迹附近。", bold=True)
    doc.P("优选地，所述钻孔数据的采样周期为0.3 s；训练样本来源于459组实际钻孔数据；参考扭矩库按照钻孔角度分别建立。")
    doc.P("优选地，所述GFTM模型对进给扭矩的预测精度R²达到0.9682，平均绝对误差MAE为0.0016，均方根误差RMSE为0.0022，相对百分比误差MAPE为1.9914%。")
    doc.P("优选地，所述模型预测控制器的控制对象为钻孔进给速度，控制目标同时考虑进给扭矩对参考轨迹的跟踪误差以及进给速度变化平滑性。")
    doc.P("与现有技术相比，本发明具有以下有益效果：")
    doc.P("1. 通过GFTM预测模型替代复杂机理建模，降低了多角度深孔钻削过程建模难度。")
    doc.P("2. 通过参考扭矩库匹配不同钻孔角度工况，解决了多姿态条件下统一参考轨迹难以适配的问题。")
    doc.P("3. 通过MPC滚动优化实现对进给速度的在线柔性调节，在正常工况及干扰工况下均具有较好的轨迹跟踪和抗扰性能。")
    doc.P("4. 在平均钻孔深度为73.6 mm、共1038个排气孔的实际加工中未出现断刀，验证了该方法的工程可行性。")

    doc.H("附图说明")
    doc.P("图1 为本发明基于GFTMPC的柔性钻孔控制系统结构框图。", indent=False)
    doc.P("图2 为本发明基于GFTMPC的柔性钻孔控制方法流程图。", indent=False)

    doc.H("具体实施方式")
    doc.P("下面结合附图和具体实施方式对本发明作进一步说明。应当理解，以下实施方式用于说明本发明而非限制本发明的保护范围。")

    doc.FIG(fig1, "图1 基于GFTMPC的柔性钻孔控制系统结构框图")
    doc.FIG(fig2, "图2 基于GFTMPC的柔性钻孔控制方法流程图")

    doc.P("S10：钻孔过程数据采集。", bold=True)
    doc.MP("在轮胎模具自动钻孔机器人系统中，以单孔加工周期为单位采集钻孔角度", s_theta, "、进给速度", s_vf, "和进给扭矩", s_tauf, "。其中，钻孔角度由机器人控制柜传输至上位机，进给速度和进给扭矩由PLC读取伺服驱动器数据后转发至上位机。优选地，采样周期设置为0.3 s。")
    doc.P("对采集到的原始数据进行滑动平均滤波处理，并按照加速钻孔阶段和稳定钻孔阶段划分样本，以削弱随机噪声并保留扭矩变化趋势。")

    doc.P("S20：参考扭矩库构建。", bold=True)
    doc.P("对不同钻孔角度下的历史钻孔数据进行对比分析，可以发现钻孔角度主要影响进给扭矩的幅值水平，而各工况下扭矩随时间变化的总体趋势保持一致。因此，本发明针对不同钻孔角度建立参考扭矩库，用于为后续控制器提供匹配当前工况的参考轨迹。")
    doc.P("优选地，从459组钻孔数据中提取进给扭矩序列，采用最小二乘法拟合各角度对应的线性参考扭矩参数，并将钻孔角度与相应参数建立映射关系，形成参考扭矩库。")

    doc.P("S30：GFTM进给扭矩预测模型构建。", bold=True)
    doc.MP("采用GRU神经网络构建进给扭矩预测模型GFTM，以钻孔角度", s_theta, "、历史进给速度", s_vf, "以及历史进给扭矩", s_tauf, "作为输入，对下一控制时刻的进给扭矩进行预测，预测关系可以表示为：")
    doc.EQ(eq_predict, "（1）")
    doc.MP("其中，", s_tauk1, "表示下一控制时刻的预测进给扭矩，", s_vk, "表示当前控制时刻的进给速度。优选地，模型训练采用Adam优化算法，训练集、验证集和测试集按7:2:1比例划分，隐藏层节点数设置为128。")
    doc.P("在本实施例中，所构建的GFTM模型预测精度R²为0.9682，说明该模型能够有效学习钻孔角度、进给速度和进给扭矩之间的动态耦合关系。")

    doc.P("S40：模型预测控制器构建。", bold=True)
    doc.MP("将参考扭矩", s_tauref, "、GFTM输出的预测扭矩以及进给速度约束引入模型预测控制器，建立滚动优化目标函数", s_j, "，用于平衡扭矩跟踪误差与控制增量平滑性，典型形式如下：")
    doc.EQ(eq_objective, "（2）")
    doc.P("其中，w1和w2分别表示扭矩跟踪项和控制增量项的权重系数。优选地，控制器同时设置进给速度上限、下限以及进给速度增量约束，以避免执行机构出现速度饱和和高频振荡。")

    doc.P("S50：柔性钻孔控制执行。", bold=True)
    doc.P("在钻孔加速阶段与稳定钻孔阶段，上位机周期性调用GFTMPC控制器，输出优化后的进给速度控制量并写入PLC，再由PLC控制直线进给机构执行。对于正常工况，控制器在满足约束条件的前提下使进给速度平稳提升并维持在高效加工区间，从而缩短单孔加工时间。")

    doc.P("S60：干扰抑制与闭环修正。", bold=True)
    doc.P("当切屑堵塞、刀具负载上升或钻孔角度变化引起外部扰动时，进给扭矩会偏离参考扭矩轨迹。控制器基于预测扭矩和参考扭矩的偏差，主动降低进给速度以减轻刀具负载，并在干扰消退后逐步恢复进给速度，使进给扭矩回归参考轨迹附近。")
    doc.P("仿真结果表明，在不同钻孔角度和不同干扰强度条件下，控制器均能在约2 s至3 s内使进给扭矩恢复稳定；在实际实验中，控制器在轻微干扰和明显干扰下仍可维持系统闭环稳定性，具备良好的实时性、稳定性和鲁棒性。")

    doc.P("实施例：", bold=True)
    doc.P("基于本发明方法，在轮胎模具自动钻孔机器人系统上对平均孔深73.6 mm的排气孔开展1038个孔的钻孔验证。系统运行过程中未出现断刀，单孔平均加工时间约17.8 s，表明本发明方法能够有效提升深孔钻削稳定性并降低断刀风险。")

    doc.P("需要说明的是，以上实施方式仅用于说明本发明的技术方案，而非对本发明保护范围的限制。本领域技术人员在不脱离本发明构思的前提下，对本发明作出的等同替换或变形，均应落入本发明的保护范围。")
    doc.save(OUT_DOCX)


def main():
    ensure_assets_dir()
    fig1 = fig_system_overview()
    fig2 = fig_method_flow()
    build_doc(fig1, fig2)


if __name__ == "__main__":
    main()

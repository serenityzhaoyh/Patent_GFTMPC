import os
import sys

os.environ.setdefault("MPLCONFIGDIR", os.path.join(os.getcwd(), ".matplotlib"))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


SKILL_SCRIPTS = r"D:\ProgramFiles\CodeTool\skills\claude-skill-patent-writing-chinese-main\scripts"
if SKILL_SCRIPTS not in sys.path:
    sys.path.insert(0, SKILL_SCRIPTS)

from patent_helpers import PatentDoc, mr, m_sub, m_sup, imath, wrap
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
    s_dvf = imath(m_sub(mr("Delta v"), mr("f")))
    s_tauref = imath(m_sub(mr("tau"), mr("ref")))
    s_taupred = imath(m_sub(mr("tau"), mr("pred")))
    s_tauk = imath(m_sub(mr("tau"), mr("k")))
    s_tauk1 = imath(m_sub(mr("tau"), mr("k+1")))
    s_vk = imath(m_sub(mr("v"), mr("k")))
    s_j = imath(mr("J"))
    s_w1 = imath(m_sub(mr("w"), mr("1")))
    s_w2 = imath(m_sub(mr("w"), mr("2")))

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
        + m_sub(mr("w"), mr("1"))
        + mr("\u00b7")
        + mr("(")
        + m_sub(mr("tau"), mr("pred"))
        + mr("-")
        + m_sub(mr("tau"), mr("ref"))
        + mr(")")
        + m_sup(mr(""), mr("2"))
        + mr("+")
        + m_sub(mr("w"), mr("2"))
        + mr("\u00b7")
        + mr("(")
        + m_sub(mr("Delta v"), mr("f"))
        + mr(")")
        + m_sup(mr(""), mr("2"))
    )

    doc.title(TITLE)

    doc.H("技术领域")
    doc.P("本发明属于轮胎模具自动钻孔与智能控制技术领域，具体涉及一种面向小直径深孔、多钻孔角度工况的基于GFTMPC的柔性钻孔控制方法及其控制系统。")

    doc.H("背景技术")
    doc.P("轮胎模具排气孔加工具有孔径小、深径比大、数量多以及钻孔方向随模具曲面法向变化的特点。传统人工钻孔、专用钻孔设备及数控机床方法难以同时兼顾加工柔性、加工稳定性与加工成本，在多角度深孔加工场景中容易出现断刀、效率低和一致性差等问题。")
    doc.P("现有钻孔控制方式大多采用固定进给参数或基于经验的分段调节策略，难以描述钻孔过程中的非线性、强耦合和时变特性。随着钻孔深度增加，切屑排出阻力、孔壁摩擦以及设备姿态变化会导致进给扭矩呈现动态波动并持续抬升，从而增加断刀风险。")
    doc.P("已有PID控制、滑模控制和自适应控制等方法在钻孔过程控制中存在模型依赖强、参数整定复杂或抗扰能力不足等问题；单纯依赖神经网络预测虽然能够捕捉部分时序规律，但通常难以同时处理执行机构约束、控制平滑性和扰动恢复过程，因此难以直接用于实际钻孔过程的在线闭环控制。")
    doc.P("此外，钻孔角度变化会显著影响进给扭矩水平，不同角度下难以采用统一的参考轨迹进行有效控制。因而，仍需要一种能够根据钻孔角度构建参考扭矩、预测未来进给扭矩并结合约束优化实时调整进给速度的柔性钻孔控制方法。")

    doc.H("发明内容")
    doc.P("本发明的目的在于提供一种基于GFTMPC的柔性钻孔控制方法及系统，以解决多钻孔角度工况下参考轨迹难以统一、进给扭矩难以准确预测以及钻孔过程抗扰性不足的问题。")
    doc.P("为实现上述目的，本发明采用如下技术方案。")
    doc.P("步骤一：采集钻孔过程中的钻孔角度、进给速度和进给扭矩数据，对数据进行滤波预处理，并按照单孔钻削周期建立钻孔过程数据集。", bold=True)
    doc.P("步骤二：基于不同钻孔角度下的历史钻孔数据，提取加速钻孔阶段和稳定钻孔阶段的进给扭矩变化规律，构建多角度参考扭矩库。", bold=True)
    doc.P("步骤三：以钻孔角度、历史进给速度和历史进给扭矩为输入，构建进给扭矩时序预测模型GFTM，用于预测下一控制时刻的进给扭矩。", bold=True)
    doc.P("步骤四：将参考扭矩、预测扭矩、进给速度约束和进给速度增量约束引入模型预测控制器，建立以扭矩跟踪误差和控制增量为目标的滚动优化问题。", bold=True)
    doc.P("步骤五：在钻孔执行过程中实时输出优化后的进给速度，并作用于钻孔加速阶段和稳定钻孔阶段，形成进给速度闭环调节。", bold=True)
    doc.P("步骤六：当外部干扰、切屑堵塞趋势或姿态变化导致进给扭矩偏离参考轨迹时，控制器依据预测结果主动调整进给速度，使进给扭矩在预定时间内回归参考轨迹附近。", bold=True)
    doc.P("优选地，所述钻孔数据的采样周期为0.3 s，采集样本来源于459组实际钻孔数据，进给速度和进给扭矩采用窗口大小为10的滑动平均法进行平滑处理。")
    doc.P("优选地，所述GFTM模型采用GRU神经网络实现，训练集、验证集和测试集按7:2:1比例划分，隐藏层节点数设置为128。")
    doc.P("优选地，所述模型预测控制器的控制对象为钻孔进给速度，控制目标同时考虑进给扭矩对参考轨迹的跟踪误差以及进给速度变化平滑性，并对进给速度上限、下限及增量范围进行约束。")
    doc.P("与现有技术相比，本发明具有以下有益效果。")
    doc.P("1. 通过建立多角度参考扭矩库匹配不同钻孔姿态工况，解决了统一参考轨迹难以适应多角度深孔加工的问题。")
    doc.P("2. 通过GFTM预测模型替代复杂机理建模，降低了多角度深孔钻削过程建模难度，并为控制器提供未来扭矩变化趋势。")
    doc.P("3. 通过MPC滚动优化实现对进给速度的在线柔性调节，可同时兼顾轨迹跟踪、控制平滑性和执行机构约束，在正常工况及干扰工况下均具有较好的抗扰性能。")
    doc.P("4. 仿真结果表明，在不同钻孔角度、不同干扰幅值和不同干扰时刻条件下，进给扭矩可在2 s至3 s内回归稳定范围；在平均钻孔深度为73.6 mm、共1038个排气孔的实际加工中未出现断刀，单孔平均加工时间约17.8 s，验证了该方法的工程可行性。")

    doc.H("附图说明")
    doc.P("图1 为本发明基于GFTMPC的柔性钻孔控制系统结构框图。", indent=False)
    doc.P("图2 为本发明基于GFTMPC的柔性钻孔控制方法流程图。", indent=False)

    doc.H("具体实施方式")
    doc.P("下面结合附图对本发明的实施方式作进一步说明。应当理解，以下实施方式仅用于说明本发明，而不用于限定本发明的保护范围。")

    doc.FIG(fig1, "图1 基于GFTMPC的柔性钻孔控制系统结构框图")
    doc.FIG(fig2, "图2 基于GFTMPC的柔性钻孔控制方法流程图")

    doc.P("S10：钻孔过程数据采集。", bold=True)
    doc.MP("以单孔加工周期为基本单元，采集钻孔角度", s_theta, "、进给速度", s_vf, "和进给扭矩", s_tauf, "。优选地，钻孔角度由机器人控制柜传输至上位机，进给速度和进给扭矩由PLC读取伺服驱动器数据后转发至上位机，采样周期设置为0.3 s。")
    doc.P("对采集到的原始数据进行滑动平均滤波处理，并按照加速钻孔阶段和稳定钻孔阶段划分样本，以削弱随机噪声并保留扭矩变化趋势。")
    doc.MP("其中，", s_theta, "表示当前孔位对应的钻孔角度，", s_vf, "表示当前进给速度，", s_tauf, "表示当前进给扭矩。")

    doc.P("S20：参考扭矩库构建。", bold=True)
    doc.P("基于不同钻孔角度下的历史钻孔数据构建参考扭矩库。由于钻孔角度主要影响进给扭矩的幅值水平，而不同工况下扭矩随时间变化的总体趋势保持一致，因此针对不同钻孔角度分别建立参考扭矩轨迹。")
    doc.P("优选地，从459组钻孔数据中提取进给扭矩序列，采用最小二乘法拟合各角度对应的线性参考扭矩参数，并将钻孔角度与相应参数建立映射关系，形成参考扭矩库。")
    doc.MP("控制执行时，根据当前钻孔角度", s_theta, "在参考扭矩库中查找或插值得到目标参考扭矩轨迹", s_tauref, "。")

    doc.P("S30：GFTM进给扭矩预测模型构建。", bold=True)
    doc.MP("采用进给扭矩时序预测模型GFTM对下一控制时刻的进给扭矩进行预测。优选地，所述GFTM采用GRU神经网络构建，并以钻孔角度", s_theta, "、历史进给速度", s_vf, "以及历史进给扭矩", s_tauf, "作为输入，预测关系可以表示为：")
    doc.EQ(eq_predict, "（1）")
    doc.MP("其中，", s_tauk1, "表示下一控制时刻的预测进给扭矩，", s_vk, "表示当前控制时刻的进给速度，", s_tauk, "表示当前控制时刻的进给扭矩。优选地，模型训练采用Adam优化算法，训练集、验证集和测试集按7:2:1比例划分，隐藏层节点数设置为128。")
    doc.P("在本实施例中，所构建的GFTM模型预测精度R²为0.9682，平均绝对误差MAE为0.0016，均方根误差RMSE为0.0022，相对百分比误差MAPE为1.9914%。")

    doc.P("S40：模型预测控制器构建。", bold=True)
    doc.MP("将参考扭矩", s_tauref, "、GFTM输出的预测扭矩以及进给速度约束引入模型预测控制器，建立滚动优化目标函数", s_j, "，用于平衡扭矩跟踪误差与控制增量平滑性，典型形式如下：")
    doc.EQ(eq_objective, "（2）")
    doc.MP("其中，", s_taupred, "表示预测进给扭矩，", s_tauref, "表示参考扭矩，", s_dvf, "表示相邻控制周期的进给速度增量，", s_w1, "和", s_w2, "分别表示扭矩跟踪项和控制增量项的权重系数。优选地，控制器同时设置进给速度上限、下限以及进给速度增量约束，以避免执行机构出现速度饱和和高频振荡。")
    doc.P("在本实施例中，针对不同干扰程度及钻孔角度开展参数整定，控制器能够在保证约束满足的前提下对进给速度进行在线滚动优化。")

    doc.P("S50：柔性钻孔控制执行。", bold=True)
    doc.P("在钻孔加速阶段与稳定钻孔阶段，上位机周期性调用GFTMPC控制器，输出优化后的进给速度控制量并写入PLC，再由PLC控制直线进给机构执行。")
    doc.P("优选地，上位机实时采集当前进给扭矩、当前进给速度和当前钻孔角度，并基于GFTMPC柔性钻孔控制算法计算下一时刻的最优进给速度；随后，经Modbus TCP与Profinet通信链路将控制指令依次传输至伺服驱动器，最终驱动直线轴电机完成进给运动调节。")

    doc.P("S60：干扰抑制与闭环修正。", bold=True)
    doc.P("当切屑堵塞、刀具负载上升或钻孔角度变化引起外部扰动时，进给扭矩会偏离参考扭矩轨迹。控制器基于预测扭矩和参考扭矩的偏差，主动降低进给速度以减轻刀具负载，并在干扰消退后逐步恢复进给速度，使进给扭矩回归参考轨迹附近。")
    doc.P("在本实施例中，在不同钻孔角度和不同干扰强度条件下，控制器均能在约2 s至3 s内使进给扭矩恢复稳定；在不同时间引入20%干扰时，系统总体响应规律保持一致并在约2 s内回归稳定状态。")

    doc.P("实施例：", bold=True)
    doc.P("在三个轮胎模具花纹块上开展实际钻孔实验，共计钻孔1038个。系统运行过程中未出现断刀，平均钻孔深度为73.6 mm，单孔平均加工时间约17.8 s。实验数据显示，无干扰钻孔比例为44.7%，轻微干扰钻孔比例为50.2%，明显干扰钻孔比例为5.1%。即使在明显干扰工况下，进给扭矩在经历短时波动后仍可回归参考轨迹附近。")

    doc.P("需要说明的是，以上实施方式仅用于说明本发明的技术方案，而非对本发明保护范围的限制。本领域技术人员在不脱离本发明构思的前提下，对本发明作出的等同替换或变形，均应落入本发明的保护范围。")

    doc.doc.add_page_break()
    doc.title("权利要求书")
    doc.P(
        "1. 一种基于GFTMPC的柔性钻孔控制方法，其特征在于，包括："
        "采集钻孔过程中的钻孔角度、进给速度和进给扭矩数据，并对所述数据进行滤波预处理；"
        "基于不同钻孔角度下的历史钻孔数据构建多角度参考扭矩库，并根据当前钻孔角度确定与当前工况匹配的参考扭矩轨迹；"
        "基于所述钻孔角度、历史进给速度和历史进给扭矩构建进给扭矩时序预测模型，以预测下一控制时刻的进给扭矩；"
        "将所述参考扭矩轨迹、预测进给扭矩、进给速度约束和进给速度增量约束输入模型预测控制器，求解以扭矩跟踪误差和控制增量为目标的滚动优化问题，得到优化后的进给速度；"
        "将所述优化后的进给速度作用于钻孔加速阶段和稳定钻孔阶段，形成进给速度闭环调节；"
        "当外部干扰、切屑堵塞趋势或姿态变化导致进给扭矩偏离所述参考扭矩轨迹时，依据预测结果调整进给速度，以使进给扭矩回归所述参考扭矩轨迹附近。"
    )
    doc.P(
        "2. 根据权利要求1所述的基于GFTMPC的柔性钻孔控制方法，其特征在于，"
        "所述采集钻孔过程中的钻孔角度、进给速度和进给扭矩数据的采样周期为0.3 s，"
        "并按照单孔钻削周期对数据进行分段，以区分钻孔加速阶段和稳定钻孔阶段。"
    )
    doc.P(
        "3. 根据权利要求1所述的基于GFTMPC的柔性钻孔控制方法，其特征在于，"
        "所述滤波预处理为对原始采集数据进行滑动平均滤波处理，以削弱随机噪声并保留进给扭矩变化趋势。"
    )
    doc.P(
        "4. 根据权利要求1所述的基于GFTMPC的柔性钻孔控制方法，其特征在于，"
        "所述多角度参考扭矩库的构建方式为：从不同钻孔角度对应的历史钻孔数据中提取进给扭矩序列，"
        "采用最小二乘法拟合各钻孔角度对应的参考扭矩参数，并建立钻孔角度与参考扭矩参数之间的映射关系。"
    )
    doc.P(
        "5. 根据权利要求1所述的基于GFTMPC的柔性钻孔控制方法，其特征在于，"
        "所述进给扭矩预测模型GFTM采用GRU神经网络构建，模型训练采用Adam优化算法，"
        "训练集、验证集和测试集按7:2:1比例划分，隐藏层节点数设置为128。"
    )
    doc.P(
        "6. 根据权利要求1所述的基于GFTMPC的柔性钻孔控制方法，其特征在于，"
        "所述模型预测控制器的目标函数同时包含预测进给扭矩与参考扭矩之间的跟踪误差项，"
        "以及进给速度增量平滑项，并对进给速度上限、进给速度下限及进给速度增量进行约束。"
    )
    doc.P(
        "7. 根据权利要求1所述的基于GFTMPC的柔性钻孔控制方法，其特征在于，"
        "当检测到切屑堵塞、刀具负载上升或钻孔角度变化引起的外部扰动时，"
        "控制器根据预测扭矩和参考扭矩的偏差降低进给速度，并在干扰消退后逐步恢复进给速度。"
    )
    doc.P(
        "8. 一种基于GFTMPC的柔性钻孔控制系统，其特征在于，包括："
        "数据采集模块，用于采集钻孔角度、进给速度和进给扭矩数据；"
        "参考扭矩库模块，用于基于不同钻孔角度下的历史钻孔数据构建多角度参考扭矩库，并根据当前钻孔角度输出与当前工况匹配的参考扭矩轨迹；"
        "GFTM进给扭矩预测模块，用于基于所述钻孔角度、历史进给速度和历史进给扭矩预测下一控制时刻的进给扭矩；"
        "模型预测控制模块，用于根据所述参考扭矩轨迹、预测进给扭矩及约束条件求解优化后的进给速度；"
        "执行控制模块，用于将所述优化后的进给速度写入钻孔执行机构，以完成柔性钻孔控制；"
        "其中，所述数据采集模块、GFTM进给扭矩预测模块、模型预测控制模块和执行控制模块形成闭环控制链路。"
    )
    doc.P(
        "9. 根据权利要求8所述的基于GFTMPC的柔性钻孔控制系统，其特征在于，"
        "所述执行控制模块包括上位机、PLC以及直线进给机构，"
        "所述上位机周期性调用模型预测控制模块输出进给速度控制量，"
        "所述PLC根据所述进给速度控制量驱动所述直线进给机构执行钻孔进给。"
    )
    doc.P(
        "10. 一种电子设备，其特征在于，包括存储器、处理器以及存储于所述存储器中并可在所述处理器上运行的计算机程序，"
        "所述处理器执行所述计算机程序时，实现权利要求1至7任一项所述的基于GFTMPC的柔性钻孔控制方法。"
    )
    doc.P(
        "11. 一种计算机可读存储介质，其上存储有计算机程序，其特征在于，"
        "所述计算机程序被处理器执行时，实现权利要求1至7任一项所述的基于GFTMPC的柔性钻孔控制方法。"
    )

    doc.doc.add_page_break()
    doc.title("说明书摘要")
    doc.P(
        "本发明公开了一种基于GFTMPC的柔性钻孔控制方法及系统，属于轮胎模具自动钻孔与智能控制技术领域。"
        "该方法采集钻孔角度、进给速度和进给扭矩数据，构建多角度参考扭矩库；"
        "利用GFTM进给扭矩时序预测模型预测下一控制时刻的进给扭矩；"
        "将参考扭矩、预测扭矩以及进给速度约束引入模型预测控制器，滚动优化得到进给速度控制量，"
        "并在钻孔加速阶段和稳定阶段进行闭环调节。"
        "当发生切屑堵塞趋势、刀具负载上升或姿态变化扰动时，控制器能够主动修正进给速度，"
        "抑制进给扭矩突增，降低深孔钻削断刀风险，提高多钻孔角度工况下的加工稳定性与一致性。"
    )
    doc.P("摘要附图：图1。", indent=False)
    doc.FIG(fig1, "图1")
    doc.save(OUT_DOCX)


def main():
    ensure_assets_dir()
    fig1 = fig_system_overview()
    fig2 = fig_method_flow()
    build_doc(fig1, fig2)


if __name__ == "__main__":
    main()

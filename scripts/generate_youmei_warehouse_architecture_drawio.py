from __future__ import annotations

from datetime import datetime, timezone, timedelta
from pathlib import Path
import xml.etree.ElementTree as ET


OUT = Path(__file__).resolve().parents[1] / "docs" / "youmei-warehouse-architecture.drawio"


PALETTE = {
    "canvas": "#F5FAF8",
    "platform": "#E8F4F1",
    "data": "#DFF0FF",
    "source": "#E7F6EA",
    "control": "#FFF2CC",
    "govern": "#F3E8FF",
    "quality": "#FFE8D6",
    "business": "#E8F5E9",
    "white": "#FFFFFF",
    "border": "#2F5F65",
    "blue": "#2F80ED",
    "orange": "#F6A400",
    "gray": "#808A94",
    "green": "#3CA370",
    "red": "#C2410C",
}


def style(fill: str, stroke: str = "#5A7A80", dashed: bool = False, font: int = 14) -> str:
    return (
        "rounded=1;whiteSpace=wrap;html=1;arcSize=6;"
        f"fillColor={fill};strokeColor={stroke};fontSize={font};"
        "fontFamily=Microsoft YaHei;align=center;verticalAlign=middle;"
        "spacing=6;spacingTop=4;spacingBottom=4;"
        + ("dashed=1;dashPattern=8 4;" if dashed else "")
    )


def lane_style(fill: str, stroke: str = "#2F5F65", dashed: bool = False) -> str:
    return (
        "rounded=1;whiteSpace=wrap;html=1;arcSize=3;"
        f"fillColor={fill};strokeColor={stroke};fontSize=16;fontStyle=1;"
        "fontFamily=Microsoft YaHei;align=center;verticalAlign=top;spacingTop=10;"
        + ("dashed=1;dashPattern=8 4;" if dashed else "")
    )


EDGE = {
    "data": f"edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor={PALETTE['blue']};strokeWidth=2;endArrow=block;endFill=1;fontFamily=Microsoft YaHei;fontSize=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5;",
    "control": f"edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor={PALETTE['orange']};strokeWidth=2;endArrow=block;endFill=1;fontFamily=Microsoft YaHei;fontSize=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5;",
    "meta": f"edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor={PALETTE['gray']};strokeWidth=2;endArrow=block;endFill=1;fontFamily=Microsoft YaHei;fontSize=12;dashed=1;dashPattern=6 4;exitX=1;exitY=0.5;entryX=0;entryY=0.5;",
    "block": f"edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor={PALETTE['red']};strokeWidth=2;endArrow=block;endFill=1;fontFamily=Microsoft YaHei;fontSize=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5;",
}


class Page:
    def __init__(self, name: str, width: int = 1800, height: int = 1100):
        self.name = name
        self.width = width
        self.height = height
        self.mx = ET.Element(
            "mxGraphModel",
            {
                "dx": "1422",
                "dy": "794",
                "grid": "1",
                "gridSize": "10",
                "guides": "1",
                "tooltips": "1",
                "connect": "1",
                "arrows": "1",
                "fold": "1",
                "page": "1",
                "pageScale": "1",
                "pageWidth": str(width),
                "pageHeight": str(height),
                "math": "0",
                "shadow": "0",
            },
        )
        self.root = ET.SubElement(self.mx, "root")
        ET.SubElement(self.root, "mxCell", {"id": "0"})
        ET.SubElement(self.root, "mxCell", {"id": "1", "parent": "0"})
        self.n = 1
        bg = ET.SubElement(
            self.root,
            "mxCell",
            {
                "id": "background",
                "value": "",
                "style": "shape=rect;html=1;fillColor=#FFFFFF;strokeColor=none;",
                "vertex": "1",
                "parent": "1",
            },
        )
        ET.SubElement(bg, "mxGeometry", {"x": "0", "y": "0", "width": str(width), "height": str(height), "as": "geometry"})

    def _id(self, prefix: str) -> str:
        self.n += 1
        return f"{prefix}-{self.n}"

    def rect(
        self,
        text: str,
        x: int,
        y: int,
        w: int,
        h: int,
        fill: str = PALETTE["white"],
        stroke: str = "#5A7A80",
        dashed: bool = False,
        font: int = 14,
        prefix: str = "n",
    ) -> str:
        cid = self._id(prefix)
        cell = ET.SubElement(
            self.root,
            "mxCell",
            {
                "id": cid,
                "value": text,
                "style": style(fill, stroke, dashed, font),
                "vertex": "1",
                "parent": "1",
            },
        )
        ET.SubElement(cell, "mxGeometry", {"x": str(x), "y": str(y), "width": str(w), "height": str(h), "as": "geometry"})
        return cid

    def lane(self, text: str, x: int, y: int, w: int, h: int, fill: str, dashed: bool = False, prefix: str = "lane") -> str:
        cid = self._id(prefix)
        cell = ET.SubElement(
            self.root,
            "mxCell",
            {
                "id": cid,
                "value": text,
                "style": lane_style(fill, dashed=dashed),
                "vertex": "1",
                "parent": "1",
            },
        )
        ET.SubElement(cell, "mxGeometry", {"x": str(x), "y": str(y), "width": str(w), "height": str(h), "as": "geometry"})
        return cid

    def edge(self, src: str, dst: str, kind: str = "data", text: str = "") -> str:
        cid = self._id("e")
        cell = ET.SubElement(
            self.root,
            "mxCell",
            {
                "id": cid,
                "value": text,
                "style": EDGE[kind],
                "edge": "1",
                "parent": "1",
                "source": src,
                "target": dst,
            },
        )
        ET.SubElement(cell, "mxGeometry", {"relative": "1", "as": "geometry"})
        return cid

    def legend(self, x: int, y: int) -> None:
        box = self.lane("图例", x, y, 250, 180, "#FFFFFF", prefix="legend")
        a = self.rect("蓝线：数据流转", x + 28, y + 45, 190, 28, "#FFFFFF", PALETTE["blue"], font=12)
        b = self.rect("黄线：控制调用", x + 28, y + 82, 190, 28, "#FFFFFF", PALETTE["orange"], font=12)
        c = self.rect("灰虚线：治理回流", x + 28, y + 119, 190, 28, "#FFFFFF", PALETTE["gray"], dashed=True, font=12)
        d = self.rect("虚线框：能力域边界", x + 28, y + 151, 190, 24, "#FFFFFF", PALETTE["border"], dashed=True, font=12)


def overall() -> Page:
    p = Page("01 目标数仓总体架构")
    p.rect("Youmei 数仓目标逻辑架构\n预策接入 + ClickHouse 分层 + Git 发布 + OpenMetadata 治理", 30, 20, 1740, 58, "#DFF6F0", PALETTE["border"], font=20)

    p.lane("业务应用层", 260, 95, 1260, 85, "#E3F4EE")
    app1 = p.rect("经营分析门户", 330, 122, 190, 36, PALETTE["business"])
    app2 = p.rect("BI 看板", 600, 122, 190, 36, PALETTE["business"])
    app3 = p.rect("数据服务接口", 870, 122, 190, 36, PALETTE["business"])
    app4 = p.rect("业务系统回流", 1140, 122, 190, 36, PALETTE["business"])

    p.lane("数据源域", 45, 220, 270, 565, "#E7F6EA", dashed=True)
    srcs = [
        p.rect("电商交易源", 90, 270, 180, 42, PALETTE["source"]),
        p.rect("营销投放源", 90, 345, 180, 42, PALETTE["source"]),
        p.rect("费用成本源", 90, 420, 180, 42, PALETTE["source"]),
        p.rect("商品店铺源", 90, 495, 180, 42, PALETTE["source"]),
        p.rect("文件/人工补充源", 90, 570, 180, 42, PALETTE["source"]),
    ]
    p.rect("源边界\n账号/店铺/批次", 90, 680, 180, 54, "#FFFFFF")

    p.lane("统一接入区", 350, 235, 235, 305, "#E8F5E9", dashed=True)
    yuce = p.rect("预策接入层", 395, 285, 145, 44, "#CDEFD6", PALETTE["green"], font=15)
    ingest_meta = p.rect("接入任务元数据", 395, 370, 145, 44, "#FFFFFF")
    batch = p.rect("批次/分区/水位", 395, 455, 145, 44, "#FFFFFF")

    p.lane("ClickHouse 数仓平台", 630, 245, 610, 540, "#EEF8FF")
    ods = p.rect("原始数据层\n(ods)", 705, 305, 150, 48, PALETTE["data"], font=15)
    dwd = p.rect("明细标准层\n(dwd)", 895, 305, 150, 48, PALETTE["data"], font=15)
    dim = p.rect("维度层\n(dim)", 1085, 305, 110, 48, PALETTE["data"], font=15)
    staging = p.rect("构建临时层\n(staging)", 705, 405, 150, 48, "#F8FBFF")
    dws = p.rect("汇总服务层\n(dws)", 895, 405, 150, 48, PALETTE["data"], font=15)
    ads = p.rect("应用数据层\n(ads)", 1085, 405, 110, 48, PALETTE["data"], font=15)
    meta = p.rect("元数据控制库\n(meta)", 760, 585, 160, 52, PALETTE["govern"])
    governed = p.rect("受治理最细可加数据集", 970, 585, 185, 52, "#FFFFFF", PALETTE["blue"])
    ckbase = p.rect("ClickHouse 存储与计算底座\n分区 / 排序键 / 物化构建 / 可重建发布", 705, 700, 450, 48, "#D6ECFF", PALETTE["blue"], font=14)

    p.lane("建模与发布控制区", 665, 815, 540, 205, PALETTE["control"], dashed=True)
    git = p.rect("Git 模型资产库", 710, 865, 150, 42, "#FFFFFF", PALETTE["orange"])
    contracts = p.rect("清洗/建模契约", 895, 845, 150, 42, "#FFFFFF", PALETTE["orange"])
    sql = p.rect("SQL/DDL/迁移", 895, 915, 150, 42, "#FFFFFF", PALETTE["orange"])
    release = p.rect("发布清单/回滚规则", 1080, 865, 150, 42, "#FFFFFF", PALETTE["orange"])
    sched = p.rect("调度编排\n依赖/重跑", 1080, 935, 150, 42, "#FFFFFF", PALETTE["orange"])

    p.lane("治理服务区", 1300, 235, 430, 305, PALETTE["govern"], dashed=True)
    om = p.rect("OpenMetadata\n元数据治理平面", 1350, 285, 170, 52, "#FFFFFF", "#7E57C2", font=15)
    catalog = p.rect("表/字段/中文名/注释", 1545, 265, 145, 42, "#FFFFFF", "#7E57C2", font=12)
    metric = p.rect("指标/枚举/血缘", 1545, 335, 145, 42, "#FFFFFF", "#7E57C2", font=12)
    version = p.rect("质量状态/生效版本", 1545, 405, 145, 42, "#FFFFFF", "#7E57C2", font=12)
    asset = p.rect("数据资产画像", 1350, 425, 170, 42, "#FFFFFF", "#7E57C2")

    p.lane("质量治理区", 1300, 600, 430, 240, PALETTE["quality"], dashed=True)
    rules = p.rect("质量规则模板", 1350, 650, 145, 42, "#FFFFFF", PALETTE["red"])
    gate = p.rect("质量门禁", 1545, 650, 145, 42, "#FFFFFF", PALETTE["red"])
    anomaly = p.rect("异常/阻断", 1350, 735, 145, 42, "#FFFFFF", PALETTE["red"])
    recon = p.rect("对账/一致性", 1545, 735, 145, 42, "#FFFFFF", PALETTE["red"])

    for s in srcs:
        p.edge(s, yuce, "data")
    p.edge(yuce, ods, "data")
    p.edge(ingest_meta, ods, "meta")
    p.edge(batch, ods, "meta")
    p.edge(ods, dwd, "data")
    p.edge(dwd, dws, "data")
    p.edge(dim, dws, "data")
    p.edge(staging, dwd, "data")
    p.edge(dws, ads, "data")
    p.edge(ads, governed, "data")
    p.edge(git, contracts, "control")
    p.edge(git, sql, "control")
    p.edge(contracts, dwd, "control")
    p.edge(sql, staging, "control")
    p.edge(release, meta, "control")
    p.edge(sched, ods, "control")
    p.edge(sched, dwd, "control")
    p.edge(sched, dws, "control")
    p.edge(sched, ads, "control")
    p.edge(rules, gate, "block")
    p.edge(gate, dwd, "block")
    p.edge(gate, dws, "block")
    p.edge(ckbase, om, "meta")
    p.edge(meta, om, "meta")
    p.edge(om, catalog, "meta")
    p.edge(om, metric, "meta")
    p.edge(om, version, "meta")
    p.edge(asset, rules, "meta")
    p.edge(ads, app1, "data")
    p.edge(ads, app2, "data")
    p.edge(governed, app3, "data")
    p.legend(1480, 875)
    return p


def data_flow() -> Page:
    p = Page("02 数据流与层级边界")
    p.rect("数据流架构\n从源域进入原始数据层，逐层标准化、汇总和消费", 30, 20, 1740, 58, "#DFF6F0", PALETTE["border"], font=20)
    x = [70, 305, 540, 775, 1010, 1245, 1480]
    labels = [
        ("源数据域", "交易/退款/费用\n商品/店铺/人工补充"),
        ("预策接入层", "接入落库\n批次与分区"),
        ("原始数据层(ods)", "保留接口交付结构\n不面向 BI"),
        ("明细标准层(dwd)", "JSON 展开\n字段清洗\n同义归并"),
        ("维度层(dim)", "商品/SKU\n店铺/达人\n直播间/时间"),
        ("汇总服务层(dws)", "商品经营\n达人经营\n直播间经营\n店铺经营"),
        ("应用数据层(ads)", "经营分析\n受治理数据集\nBI 消费"),
    ]
    ids = []
    for i, (title, body) in enumerate(labels):
        p.lane(title, x[i], 150, 190, 650, "#EEF8FF" if i >= 2 else "#E8F5E9")
        ids.append(p.rect(body, x[i] + 25, 230, 140, 130, PALETTE["white"], font=13))
    for i in range(len(ids) - 1):
        p.edge(ids[i], ids[i + 1], "data")

    stg = p.rect("构建临时层(staging)\n重建/校验/切换前承接", 650, 570, 220, 70, "#FFFFFF", "#5A7A80")
    q1 = p.rect("源完整性", 430, 435, 120, 42, PALETTE["quality"], PALETTE["red"])
    q2 = p.rect("主键唯一", 660, 435, 120, 42, PALETTE["quality"], PALETTE["red"])
    q3 = p.rect("类型解析", 890, 435, 120, 42, PALETTE["quality"], PALETTE["red"])
    q4 = p.rect("汇总对账", 1130, 435, 120, 42, PALETTE["quality"], PALETTE["red"])
    q5 = p.rect("消费一致性", 1365, 435, 120, 42, PALETTE["quality"], PALETTE["red"])
    p.edge(q1, ids[2], "block")
    p.edge(q2, ids[3], "block")
    p.edge(q3, ids[3], "block")
    p.edge(q4, ids[5], "block")
    p.edge(q5, ids[6], "block")
    p.edge(stg, ids[3], "data")
    p.edge(stg, ids[5], "data")

    c = p.lane("跨层治理回流", 350, 845, 1070, 175, PALETTE["govern"], dashed=True)
    git = p.rect("Git 契约/SQL/发布清单", 405, 900, 210, 50, "#FFFFFF", PALETTE["orange"])
    om = p.rect("OpenMetadata\n资产/字段/指标/血缘", 765, 900, 210, 50, "#FFFFFF", "#7E57C2")
    meta = p.rect("ClickHouse 元数据控制库(meta)\n版本指针/运行批次", 1125, 900, 230, 50, "#FFFFFF", "#7E57C2")
    p.edge(git, stg, "control")
    p.edge(ids[2], om, "meta")
    p.edge(ids[3], om, "meta")
    p.edge(ids[5], om, "meta")
    p.edge(meta, ids[6], "meta")
    p.legend(1490, 845)
    return p


def governance() -> Page:
    p = Page("03 发布治理闭环")
    p.rect("控制流与治理架构\n模型资产可重建，质量门禁可阻断，治理信息可回写", 30, 20, 1740, 58, "#DFF6F0", PALETTE["border"], font=20)
    git = p.lane("Git 模型资产与发布规则中枢", 80, 145, 390, 420, PALETTE["control"], dashed=True)
    assets = [
        p.rect("清洗契约", 125, 210, 130, 42, "#FFFFFF", PALETTE["orange"]),
        p.rect("建模契约", 300, 210, 130, 42, "#FFFFFF", PALETTE["orange"]),
        p.rect("模型 SQL", 125, 295, 130, 42, "#FFFFFF", PALETTE["orange"]),
        p.rect("DDL/迁移脚本", 300, 295, 130, 42, "#FFFFFF", PALETTE["orange"]),
        p.rect("质量测试", 125, 380, 130, 42, "#FFFFFF", PALETTE["orange"]),
        p.rect("元数据契约", 300, 380, 130, 42, "#FFFFFF", PALETTE["orange"]),
        p.rect("血缘定义", 125, 465, 130, 42, "#FFFFFF", PALETTE["orange"]),
        p.rect("发布清单", 300, 465, 130, 42, "#FFFFFF", PALETTE["orange"]),
    ]
    sched = p.lane("调度编排", 560, 145, 300, 420, "#FFF7DB", dashed=True)
    s1 = p.rect("落库检测", 610, 210, 190, 42, "#FFFFFF", PALETTE["orange"])
    s2 = p.rect("依赖编排", 610, 295, 190, 42, "#FFFFFF", PALETTE["orange"])
    s3 = p.rect("失败重跑", 610, 380, 190, 42, "#FFFFFF", PALETTE["orange"])
    s4 = p.rect("回滚重建", 610, 465, 190, 42, "#FFFFFF", PALETTE["orange"])

    ck = p.lane("ClickHouse 构建与生效", 950, 145, 390, 420, "#EEF8FF")
    staging = p.rect("构建临时层(staging)", 1005, 210, 160, 42, PALETTE["white"])
    gate = p.rect("质量门禁", 1175, 295, 130, 42, PALETTE["quality"], PALETTE["red"])
    formal = p.rect("正式数仓层\nods/dwd/dim/dws/ads", 1005, 380, 160, 58, PALETTE["data"], PALETTE["blue"])
    meta = p.rect("元数据控制库(meta)\n生效版本/运行批次", 1175, 455, 150, 58, PALETTE["govern"], "#7E57C2", font=12)

    gov = p.lane("OpenMetadata 治理平面", 1430, 145, 300, 420, PALETTE["govern"], dashed=True)
    om = p.rect("表资产与字段", 1485, 210, 190, 42, "#FFFFFF", "#7E57C2")
    m1 = p.rect("中文名/注释/标签", 1485, 285, 190, 42, "#FFFFFF", "#7E57C2")
    m2 = p.rect("枚举/指标口径", 1485, 360, 190, 42, "#FFFFFF", "#7E57C2")
    m3 = p.rect("血缘/质量状态/版本", 1485, 435, 190, 42, "#FFFFFF", "#7E57C2")

    for a in assets:
        p.edge(a, s2, "control")
    p.edge(s1, staging, "control")
    p.edge(s2, staging, "control")
    p.edge(staging, gate, "data")
    p.edge(gate, formal, "block")
    p.edge(formal, meta, "meta")
    p.edge(s3, staging, "control")
    p.edge(s4, staging, "control")
    p.edge(meta, formal, "control")
    p.edge(formal, om, "meta")
    p.edge(assets[5], m1, "meta")
    p.edge(assets[6], m3, "meta")
    p.edge(meta, m3, "meta")
    p.edge(om, m1, "meta")
    p.edge(om, m2, "meta")
    p.edge(om, m3, "meta")

    p.lane("固化原则", 280, 665, 1240, 215, "#FFFFFF", dashed=True)
    p.rect("不靠保留多张正式表做版本\n靠 Git 中可重建规则 + 发布清单回滚", 340, 735, 320, 70, "#FFFFFF", PALETTE["border"])
    p.rect("质量失败先阻断生效\n异常统计和人工确认进入契约版本", 740, 735, 320, 70, "#FFFFFF", PALETTE["border"])
    p.rect("OpenMetadata 记录当前生效模型版本\n字段、枚举、指标、血缘同步登记", 1140, 735, 320, 70, "#FFFFFF", PALETTE["border"])
    p.legend(1490, 820)
    return p


def business_model() -> Page:
    p = Page("04 抖店经营分析主题架构")
    p.rect("抖店经营分析主题模型\n销售、退款、费用、成本、利润通过一致维度进入可分析数据集", 30, 20, 1740, 58, "#DFF6F0", PALETTE["border"], font=20)
    p.lane("业务过程事实", 70, 150, 310, 580, PALETTE["business"], dashed=True)
    f_sales = p.rect("销售事实\n订单商品明细", 125, 215, 200, 50, "#FFFFFF", PALETTE["green"])
    f_refund = p.rect("退款事实\n售后/退货退款", 125, 310, 200, 50, "#FFFFFF", PALETTE["green"])
    f_fee = p.rect("推广费用事实\n投放/联盟/其他费用", 125, 405, 200, 50, "#FFFFFF", PALETTE["green"])
    f_live = p.rect("直播间/达人费用事实\n按直播间、达人归因", 125, 500, 200, 58, "#FFFFFF", PALETTE["green"])
    f_cost = p.rect("成本事实\n商品成本/履约成本", 125, 610, 200, 50, "#FFFFFF", PALETTE["green"])

    p.lane("DWD 经营明细口径", 485, 150, 360, 580, "#EEF8FF")
    dwd_order = p.rect("订单商品明细事实(dwd)\n店铺订单号 + 商品明细序号", 555, 235, 220, 62, PALETTE["data"], PALETTE["blue"])
    attr = p.rect("费用归因/分摊口径\n订单/商品/直播间/达人", 555, 370, 220, 62, "#FFFFFF", PALETTE["blue"])
    profit = p.rect("利润口径\n销售 - 退款 - 费用 - 成本", 555, 505, 220, 62, "#FFFFFF", PALETTE["blue"])
    atomic = p.rect("最细可加经营数据集\n供筛选后自动汇总", 555, 625, 220, 62, "#FFFFFF", PALETTE["blue"])

    p.lane("一致维度", 940, 150, 310, 580, "#F3E8FF", dashed=True)
    dims = [
        p.rect("商品/SKU", 995, 215, 200, 42, "#FFFFFF", "#7E57C2"),
        p.rect("店铺", 995, 295, 200, 42, "#FFFFFF", "#7E57C2"),
        p.rect("达人", 995, 375, 200, 42, "#FFFFFF", "#7E57C2"),
        p.rect("直播间", 995, 455, 200, 42, "#FFFFFF", "#7E57C2"),
        p.rect("时间", 995, 535, 200, 42, "#FFFFFF", "#7E57C2"),
        p.rect("渠道/活动", 995, 615, 200, 42, "#FFFFFF", "#7E57C2"),
    ]
    dim_bus = p.rect("一致维度口径总线", 995, 690, 200, 42, "#FFFFFF", "#7E57C2")

    p.lane("主题服务与应用消费", 1340, 150, 360, 580, "#FFF7DB", dashed=True)
    dws1 = p.rect("商品经营主题(dws)", 1405, 220, 230, 42, "#FFFFFF", PALETTE["orange"])
    dws2 = p.rect("达人经营主题(dws)", 1405, 305, 230, 42, "#FFFFFF", PALETTE["orange"])
    dws3 = p.rect("直播间经营主题(dws)", 1405, 390, 230, 42, "#FFFFFF", PALETTE["orange"])
    dws4 = p.rect("店铺经营主题(dws)", 1405, 475, 230, 42, "#FFFFFF", PALETTE["orange"])
    ads = p.rect("经营分析应用(ads)\n销售/退款/费用/成本/利润", 1405, 585, 230, 62, "#FFFFFF", PALETTE["orange"])

    for f in [f_sales, f_refund, f_fee, f_live, f_cost]:
        p.edge(f, dwd_order if f == f_sales else attr, "data")
    p.edge(dwd_order, attr, "data")
    p.edge(attr, profit, "data")
    p.edge(profit, atomic, "data")
    p.edge(atomic, dim_bus, "meta")
    for dws in [dws1, dws2, dws3, dws4]:
        p.edge(atomic, dws, "data")
        p.edge(dws, ads, "data")

    p.lane("关键建模边界", 220, 805, 1360, 170, "#FFFFFF", dashed=True)
    p.rect("DWD 保留最细事实和清洗后的统一字段\n不把报表字段反推为上游事实", 280, 865, 330, 62, "#FFFFFF", PALETTE["border"])
    p.rect("DWS 可按商品、达人、直播间、店铺拆主题\n每张表必须声明主粒度", 730, 865, 330, 62, "#FFFFFF", PALETTE["border"])
    p.rect("ADS 面向看板消费\n只读受治理数据集，不直接读取原始数据层(ods)", 1180, 865, 330, 62, "#FFFFFF", PALETTE["border"])
    p.legend(1510, 835)
    return p


def build() -> None:
    mxfile = ET.Element(
        "mxfile",
        {
            "host": "app.diagrams.net",
            "modified": datetime.now(timezone(timedelta(hours=8))).isoformat(timespec="seconds"),
            "agent": "Codex",
            "version": "24.7.17",
            "type": "device",
        },
    )
    for page in [overall(), data_flow(), governance(), business_model()]:
        diagram = ET.SubElement(mxfile, "diagram", {"id": page.name, "name": page.name})
        diagram.append(page.mx)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    ET.indent(mxfile, space="  ")
    ET.ElementTree(mxfile).write(OUT, encoding="utf-8", xml_declaration=True)
    print(OUT)


if __name__ == "__main__":
    build()

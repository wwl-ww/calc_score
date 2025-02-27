import json
import warnings
import gradio as gr
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False

warnings.filterwarnings("ignore", category=UserWarning)

DEFAULT_DATA = pd.read_excel("course.xlsx").values.tolist()

with open("config.json", "r") as jsonfile:
    config = json.load(jsonfile)


def process_data(input_data):
    
    # 将输入的表格数据转换为 DataFrame
    df = pd.DataFrame(input_data)
    # 把""转换为np.nan
    df.replace("", np.nan, inplace=True)
    # 如果输入数据部分有空缺，则使用对应位置的默认数据
    # ? gradio第二次启动时，会自动去除之前所有的默认数据，所以这里必须手动填充
    for i in range(len(DEFAULT_DATA)):
        for j in range(len(DEFAULT_DATA[i])):
            if not df.iloc[i, j]:
                df.iloc[i, j] = DEFAULT_DATA[i][j]
    
    df = df.dropna()
    df["原始成绩"] = df["原始成绩"].astype(float)
    df["学分"] = df["学分"].astype(float)

    mean_score = np.dot(df["原始成绩"], df["学分"]) / df["学分"].sum()
    mean_score = np.around(mean_score, config["precision"]["mean_score"])

    df["拉分效益"] = (df["原始成绩"] - mean_score) * df["学分"]
    df["拉分效益"] = df["拉分效益"].round(config["precision"]["gain"])
    df = df.sort_values("拉分效益", ascending=False)
    
    # 删除空缺行
    df = df.dropna()
    df = df.reset_index(drop=True)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 8), sharex=True)

    ax1.bar(df["课程名称"], df["原始成绩"], color=config["color"]["score"], width=0.5)
    ax1.axhline(
        y=mean_score,
        color="red",
        linestyle="--",
        linewidth=2,
        label=f"平均分: {mean_score:.2f}",
    )
    ax1.set_title("原始成绩", fontsize=14, fontweight="bold")
    ax1.set_ylabel("成绩", fontsize=12)
    ax1.set_xticklabels(df["课程名称"], rotation=config["rotation_x"], fontsize=10)
    ax1.legend(fontsize=10)
    # ax1.grid(axis="y", linestyle="--", alpha=0.7)
    ax1.set_ylim(60, 100)

    ax2.bar(df["课程名称"], df["拉分效益"], color=config["color"]["gain"], width=0.5)
    ax2.axhline(y=0, color="red", linestyle="-", linewidth=2, label="基准线: 0")
    ax2.set_title("拉分效益", fontsize=14, fontweight="bold")
    ax2.set_xlabel("课程名称", fontsize=12)
    ax2.set_ylabel("效益", fontsize=12)
    ax2.set_xticklabels(df["课程名称"], rotation=45, fontsize=10)
    ax2.legend(fontsize=10)
    # ax2.grid(axis="y", linestyle="--", alpha=0.7)
    # ax2.set_ylim(-100, 100)

    # plt.figure(figsize=(10, 6))
    # plt.bar(df["课程名称"], df["原始成绩"], width=0.5)
    # plt.bar(df["课程名称"], df["拉分效益"], width=0.5)
    # plt.axhline(y=mean_score, color="red", linestyle="--", label=f"平均分: {mean_score}")
    # # plt.ylim(60, 100)  # y 轴范围
    # plt.xlabel("课程名称", fontsize=14)
    # plt.ylabel("成绩", fontsize=14)
    # plt.title("课程成绩柱状图", fontsize=16)
    # plt.xticks(rotation=45, fontsize=12)  # 旋转 x 轴标签，防止重叠
    # plt.legend()  # 添加图例
    # plt.tight_layout()
    
    return mean_score, df, plt


def main():
    demo = gr.Interface(
        fn=process_data,
        inputs=gr.Dataframe(
            headers=["课程名称", "学分", "原始成绩"],  # 表格的列名
            datatype=["str", "number", "number"],  # 列数据类型
            label="输入课程、学分和成绩信息",
            interactive=True,
            row_count=(18, "dynamic"),  # 动态行数，至少4行
            col_count=(3, "fixed"),  # 固定列数
            value=DEFAULT_DATA,
        ),
        outputs=[
            gr.Number(label="均分"),
            gr.Dataframe(label="分数分析"),
            gr.Plot(label="成绩分析图"),
        ],
        title="均分分析器",
        description="输入表格，然后点击提交，即可计算均分和成绩分析。",
        flagging_options=None,  # 禁用 Flag 按钮
    )

    # 启动界面
    demo.launch(share=config["share"])


if __name__ == "__main__":
    main()

from pyecharts.charts import Map, WordCloud, Bar
from pyecharts import options as opts

# 在文件顶部添加数据常量
HEATMAP_DATA = [
    ("黄浦区", 9823567),
    ("徐汇区", 6754321),
    ("长宁区", 5342198),
    ("静安区", 8234156),
    ("普陀区", 4678912),
    ("虹口区", 3897654),
    ("杨浦区", 6213456),
    ("浦东新区", 12345678),
    ("闵行区", 5876342),
    ("宝山区", 4567891),
    ("嘉定区", 3789123),
    ("金山区", 2678901),
    ("松江区", 3345678),
    ("青浦区", 2987654),
    ("奉贤区", 2156789),
    ("崇明区", 1789012)
]

WORDCLOUD_DATA = [
    ("学区房", 100), 
    ("地铁房", 85),
    ("精装修", 78),
    ("朝南", 65),
    ("两室一厅", 60),
    ("低楼层", 45)]

HISTOGRAM_DATA = [
    ("万科城市花园", 245),
    ("碧桂园凤凰城", 189),
    ("朝南", 65),
    ("两室一厅", 60),
    ("低楼层", 45)]

# 修改生成函数使用本地数据
def generate_heat_map():
    chart = (
        Map(init_opts=opts.InitOpts(width="100%", height="500px"))
        .add("总价", data_pair=HEATMAP_DATA, maptype="上海")
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title="上海市二手房总价分布",
                pos_left="center",  # 标题居中
                title_textstyle_opts=opts.TextStyleOpts(
                    font_size=18,    # 字体大小
                    color="#333",    # 字体颜色
                    font_weight="bold"  # 加粗
                )
            ),
            legend_opts=opts.LegendOpts(is_show=False),
            visualmap_opts=opts.VisualMapOpts(
                min_=min(d[1] for d in HEATMAP_DATA),
                max_=max(d[1] for d in HEATMAP_DATA),
                range_color=['#e6f7ff', '#1890ff'],
                is_show=True,
                is_piecewise=False,
                orient='vertical',
                pos_top="20%",
                pos_left="5%",
                range_text=['高', '低'],
                out_of_range={'color': '#fff'}
            )
        )
    )
    return chart

def generate_wordcloud():
    chart = (
        WordCloud()
        .add(series_name="", data_pair=WORDCLOUD_DATA, word_size_range=[15, 50])
        .set_global_opts(  # 新增标题配置
            title_opts=opts.TitleOpts(
                title="房源标签词云",
                pos_left="center",
                title_textstyle_opts=opts.TextStyleOpts(font_weight="bold")
            )
        )
    )
    return chart

def generate_histogram():
    sorted_data = sorted(HISTOGRAM_DATA, key=lambda x: x[1], reverse=True)[:10]
    chart = (
        Bar(init_opts=opts.InitOpts(width="100%", height="400px"))
        .add_xaxis([x[0] for x in sorted_data])
        .add_yaxis(
            series_name="房源数量",
            y_axis=[x[1] for x in sorted_data],
            label_opts=opts.LabelOpts(is_show=False)
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title="小区房源数量TOP10",
                pos_left="center",  # 新增居中配置
                title_textstyle_opts=opts.TextStyleOpts(font_weight="bold")  # 可选加粗
            ),
            legend_opts=opts.LegendOpts(is_show=False),
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-45)),
            datazoom_opts=[opts.DataZoomOpts()]
        )
    )
    return chart

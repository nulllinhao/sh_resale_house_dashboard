from pyecharts.charts import Map, WordCloud, Bar, Line
from pyecharts import options as opts
from spider.data_handler import get_handler
from sqlalchemy import func
from collections import Counter

# 初始化数据库连接
DB_HANDLER = get_handler(
    'mysql',
    repo_name='sh_resale_house',
    url='mysql+pymysql://root:root@localhost/scraping_db',
)
HOUSE_TABLE = DB_HANDLER.table

def generate_heat_map():
    # 获取各行政区总价数据
    result = DB_HANDLER.session.query(
        HOUSE_TABLE.distinct,
        func.sum(HOUSE_TABLE.price)
    ).group_by(HOUSE_TABLE.distinct).all()
    
    chart = (
        Map(init_opts=opts.InitOpts(width="100%", height="800px"))
        .add("总价", data_pair=result, maptype="上海")
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title="上海市二手房总价分布",
                pos_left="center",
                title_textstyle_opts=opts.TextStyleOpts(font_weight="bold")
            ),
            legend_opts=opts.LegendOpts(is_show=False),
            visualmap_opts=opts.VisualMapOpts(
                min_=min(d[1] for d in result),
                max_=max(d[1] for d in result),
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
    # 获取标签词频数据
    all_tags = []
    records = DB_HANDLER.session.query(HOUSE_TABLE.tag).all()
    for tag_str, in records:
        all_tags.extend(tag_str.split(', '))
    word_counts = Counter(all_tags)
    
    chart = (
        WordCloud()
        .add(series_name="", data_pair=word_counts.most_common(20), word_size_range=[15, 50])
        .set_global_opts(  # 新增标题配置
            title_opts=opts.TitleOpts(
                title="二手房标签词云",
                pos_left="center",
                title_textstyle_opts=opts.TextStyleOpts(font_weight="bold")
            )
        )
    )
    return chart

def generate_histogram():
    # 获取行政区二手房数量数据
    result = DB_HANDLER.session.query(
        HOUSE_TABLE.distinct,
        func.count(HOUSE_TABLE.distinct)
    ).group_by(HOUSE_TABLE.distinct).order_by(func.count(HOUSE_TABLE.distinct).desc()).limit(10).all()
    
    chart = (
        Bar(init_opts=opts.InitOpts(width="100%", height="400px"))
        .add_xaxis([x[0] for x in result])
        .add_yaxis(series_name="二手房数量", y_axis=[x[1] for x in result])
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title="行政区二手房数量TOP10",
                pos_left="center",
                title_textstyle_opts=opts.TextStyleOpts(font_weight="bold")
            ),
            legend_opts=opts.LegendOpts(is_show=False),
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-45)),
            datazoom_opts=[opts.DataZoomOpts()]
        )
    )
    return chart

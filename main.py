from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
from pyecharts.charts import Map
from pyecharts import options as opts
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# 添加数据库配置（根据实际修改）
DATABASE_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "root",
    "database": "scraping_db"
}

# 创建数据库引擎
engine = create_engine(
    f"mysql+pymysql://{DATABASE_CONFIG['user']}:{DATABASE_CONFIG['password']}"
    f"@{DATABASE_CONFIG['host']}:{DATABASE_CONFIG['port']}/{DATABASE_CONFIG['database']}"
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_heat_map():
    # 模拟上海各行政区数据
    data = [
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

    # 创建上海行政区热力图
    chart = (
        Map(init_opts=opts.InitOpts(width="100%", height="800px"))
        .add("总价", 
             data_pair=data,
             maptype="上海",
             is_map_symbol_show=False)
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
                min_=min(d[1] for d in data),
                max_=max(d[1] for d in data),
                range_color=['#e6f7ff', '#1890ff'],
                is_show=True,
                is_piecewise=False,
                orient='vertical',
                pos_top="20%",
                pos_left="5%",
                range_text=['高', '低'],
                # 修改为兼容性写法
                out_of_range={'color': '#fff'}  # 直接使用字典格式配置
            )
        )
    )
    return chart

@app.get("/")
async def auto_render():
    chart = create_heat_map()
    return templates.TemplateResponse(
        "index.html",
        {
            "request": {},  # FastAPI 模板需要保留request参数
            "title": "上海市二手房数据可视化",
            "chart": chart.render_embed(),
            "js_files": chart.js_dependencies.items
        }
    )

if __name__ == "__main__":
    uvicorn.run(app)
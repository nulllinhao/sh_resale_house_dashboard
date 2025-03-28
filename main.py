from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
import uvicorn
from utils.chart_generator import generate_heat_map, generate_wordcloud, generate_histogram

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def root():
    heatmap = generate_heat_map()
    wordcloud = generate_wordcloud()
    histogram = generate_histogram()
    return templates.TemplateResponse(
        "index.html",
        {
            "request": {},
            "title": "上海市二手房数据可视化",
            "chart": heatmap.render_embed(),
            "wordcloud": wordcloud.render_embed(),
            "histogram": histogram.render_embed(),
            "js_files": heatmap.js_dependencies.items + wordcloud.js_dependencies.items
        }
    )

if __name__ == "__main__":
    uvicorn.run(app)
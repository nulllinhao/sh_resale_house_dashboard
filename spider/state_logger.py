import json
import os

# 定义状态保存文件路径
state_file = "state.json"

# 保存运行状态到文件
def save_state(next_page, next_index):
    state = {
        "next_page": next_page,
        "next_index": next_index,
    }
    with open(state_file, "w") as f:
        json.dump(state, f)

# 加载运行状态
def load_state():
    if os.path.exists(state_file):
        with open(state_file, "r") as f:
            return json.load(f)
    return None

# 删除状态文件（任务完成时）
def clear_state():
    if os.path.exists(state_file):
        os.remove(state_file)
import tracemalloc
from fastapi import FastAPI

app = FastAPI()

# 在应用启动时开启内存追踪
@app.on_event("startup")
def startup_event():
    tracemalloc.start()

# 定义一个路由来返回内存分配的统计信息
@app.get("/memory")
def get_memory_usage():
    # 截取当前内存快照
    snapshot = tracemalloc.take_snapshot()
    # 按照代码行号统计内存分配情况
    top_stats = snapshot.statistics('lineno')

    # 取出前 10 个内存使用最多的代码行
    result = []
    for stat in top_stats[:10]:
        result.append(str(stat))
    return {"top_allocations": result}


if __name__ == '__main__':
    # 第一种启动方式：
    # 如需启动，在终端 输入命令 ：
    #    fastapi dev fastapi_basics.py  （命令 fastapi dev 读取您的 main.py 文件，检测其中的 FastAPI 应用程序，并使用 Uvicorn 启动服务器。）
    # - http://127.0.0.1:8000/docs

    # 第二种启动方式：
    # pip install uvicorn
    import uvicorn

    uvicorn.run(app, host='127.0.0.1', port=8000)

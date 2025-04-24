#模型下载
from modelscope import snapshot_download
model_dir = snapshot_download('BAAI/bge-large-zh-v1.5', cache_dir='./bge-large-zh-v1.5')
print(model_dir)

model_dir = snapshot_download('BAAI/bge-reranker-large', cache_dir='./bge-reranker-large')
print(model_dir)

#模型下载
from modelscope import snapshot_download
model_dir = snapshot_download('BAAI/bge-small-zh-v1.5', cache_dir='./bge-small-zh-v1.5')
print(model_dir)

model_dir = snapshot_download('BAAI/bge-reranker-base', cache_dir='./bge-reranker-base')
print(model_dir)

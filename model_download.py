#模型下载
from modelscope import snapshot_download
model_dir = snapshot_download('BAAI/bge-large-zh-v1.5', cache_dir='/media/zj/data2-ext4/BAAI/bge-large-zh-v1.5')
print(model_dir)

model_dir = snapshot_download('BAAI/bge-reranker-large', cache_dir='/media/zj/data2-ext4/BAAI/bge-reranker-large')
print(model_dir)


#!/bin/bash -e

NODE_DIR=$PWD/node
MODEL_DIR=$PWD/model

rm -rf $NODE_DIR
mkdir $NODE_DIR

curl -sSfL 'https://github.com/GaiaNet-AI/gaianet-node/releases/latest/download/install.sh' | bash -s -- --base $NODE_DIR
export PATH="$NODE_DIR/bin:$PATH"

gsutil cp ./config.json gs://xtreamly-906e5.appspot.com
gaianet init --base $NODE_DIR --config "https://firebasestorage.googleapis.com/v0/b/xtreamly-906e5.appspot.com/o/config.json?alt=media"

rm -rf $MODEL_DIR
mkdir $MODEL_DIR

curl -sSf https://raw.githubusercontent.com/WasmEdge/WasmEdge/master/utils/install_v2.sh | bash -s
curl -L -o $MODEL_DIR/nomic-embed-text-v1.5.f16.gguf https://huggingface.co/gaianet/Nomic-embed-text-v1.5-Embedding-GGUF/resolve/main/nomic-embed-text-v1.5.f16.gguf

mkdir $MODEL_DIR/qdrant_storage
mkdir $MODEL_DIR/qdrant_snapshots

nohup docker run -d -p 6333:6333 -p 6334:6334 \
    -v $MODEL_DIR/qdrant_storage:/qdrant/storage:z \
    -v $MODEL_DIR/qdrant_snapshots:/qdrant/snapshots:z \
    qdrant/qdrant
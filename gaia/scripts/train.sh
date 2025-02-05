#!/bin/bash -e

DIR=$PWD/model

curl -X DELETE 'http://localhost:6333/collections/default'

curl -X PUT 'http://localhost:6333/collections/default' \
  -H 'Content-Type: application/json' \
  --data-raw '{
    "vectors": {
      "size": 768,
      "distance": "Cosine",
      "on_disk": true
    }
  }'

curl -L -o $DIR/paragraph_embed.wasm https://github.com/GaiaNet-AI/embedding-tools/raw/main/paragraph_embed/paragraph_embed.wasm

wasmedge --dir .:. \
  --nn-preload embedding:GGML:AUTO:$DIR/nomic-embed-text-v1.5.f16.gguf \
  $DIR/paragraph_embed.wasm embedding default 768 knowledge.txt -c 32768

response=$(curl -X POST 'http://localhost:6333/collections/default/snapshots')
snapshot_name=$(echo "$response" | jq -r '.result.name')

gsutil cp ./model/qdrant_snapshots/default/$snapshot_name gs://xtreamly-906e5.appspot.com/default.snapshot


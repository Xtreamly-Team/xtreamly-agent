# Xtreamly <> Gaia AI Agent

This is a custom Gaia agent instilled with Xtreamly's AI intelligent knowledge on Crypto market volatility predictions.

## Prerequisites

* OSX with Apple Silicon (M1-M4 chip)	16GB RAM (32GB recommended)
* Ubuntu Linux 20.04 with Nvidia CUDA 12 SDK	8GB VRAM on GPU
* Azure/AWS	Nvidia T4 GPU Instance
* Install gsutil: https://cloud.google.com/storage/docs/gsutil_install

## Local setup

1. Initialize Gaianet and Model training
```bash
./scripts/init.sh
```

2. Start Gaianet node
```bash
./scripts/start.sh
```

## Training a model

Currently this code base can train a model providing a simple .txt file.

1. In `./knowledge.txt` add the knowledge, in plain text, of your AI agent
2. Execute the train command:
```bash
./scripts/train.sh
```



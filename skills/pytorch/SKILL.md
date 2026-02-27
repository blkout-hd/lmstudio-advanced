# PyTorch ML Workflow

> Skill for PyTorch model training, fine-tuning, and evaluation pipelines.
> Sourced from Smithery registry (pytorch-authored / community).

## When to Use

Use this skill when:
- Fine-tuning HuggingFace models (LEGAL-BERT, Qwen3, etc.) on domain data
- Writing or debugging PyTorch training loops
- Evaluating model checkpoints and exporting to GGUF/SafeTensors
- Setting up CUDA-accelerated data pipelines with `torch.utils.data`

## Workflow

1. Define dataset and DataLoader (HuggingFace `datasets` + `transformers`)
2. Initialize model from HF hub or local checkpoint
3. Configure optimizer, scheduler, and mixed-precision scaler
4. Train loop with gradient accumulation and checkpoint saving
5. Evaluate on held-out set (F1, accuracy, BLEU depending on task)
6. Export: `model.save_pretrained()` + optionally convert to GGUF via `llama.cpp`

## Key Tools

- `transformers`, `datasets`, `peft`, `trl` (for SFT/DPO)
- `accelerate` for multi-GPU / mixed precision
- `llama.cpp` convert scripts for GGUF export
- `unsloth` for fast QLoRA fine-tuning on 4-8B models

## Smithery Install

```bash
npx @smithery/cli install pytorch/training-workflow
```

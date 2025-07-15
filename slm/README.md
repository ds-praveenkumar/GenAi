---
language: en
license: mit
tags:
  - text-generation
  - gpt2
  - causal-lm
  - shakespeare
  - small-model
---

# 🧠 SLM-GPT2: Tiny Shakespeare GPT-2 Model

`SLM-GPT2` is a small GPT-2-like language model trained from scratch on the [Tiny Shakespeare dataset](https://huggingface.co/datasets/tiny_shakespeare). It’s a toy model meant for educational purposes, experimentation, and understanding how transformer-based language models work.

---

## ✨ Model Details

- **Architecture**: GPT-2 (custom config)
- **Layers**: 4
- **Hidden size**: 256
- **Heads**: 4
- **Max sequence length**: 128
- **Vocabulary size**: Same as tokenizer (based on `distilgpt2` or custom)
- **Training epochs**: 3
- **Dataset**: [tiny_shakespeare](https://huggingface.co/datasets/tiny_shakespeare)

---

## 🧪 Intended Use

- Educational demos
- Debugging/training pipeline validation
- Low-resource inference tests
- Not suitable for production or accurate text generation

---

## 🚫 Limitations

- Trained on a tiny dataset (~100 KB)
- Limited vocabulary and generalization
- Can generate incoherent or biased outputs
- Not safe for deployment in real-world applications

---

## 💻 How to Use

```python
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

model = AutoModelForCausalLM.from_pretrained("your-username/slm-gpt2")
tokenizer = AutoTokenizer.from_pretrained("your-username/slm-gpt2")

generator = pipeline("text-generation", model=model, tokenizer=tokenizer)
output = generator("To be or not to be", max_length=50)
print(output[0]['generated_text'])
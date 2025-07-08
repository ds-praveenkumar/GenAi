
from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForCausalLM, Trainer, TrainingArguments, GPT2Config, GPT2LMHeadModel, pipeline
import torch 
torch.set_default_dtype(torch.float32) 

class SLMGPT2:
    def __init__(self, tokenizer_id, model_id):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.dataset = load_dataset("tiny_shakespeare", trust_remote_code=True)
        self.tokenizer = AutoTokenizer.from_pretrained(tokenizer_id)
        self.tokenizer.add_special_tokens({'pad_token': '[PAD]'})
        self.distilled_model = AutoModelForCausalLM.from_pretrained(model_id)
        self.vocab_size=self.tokenizer.vocab_size
        self.n_positions=128
        self.n_ctx=128
        self.n_embd=256
        self.n_layer=4
        self.n_head=4
        print(f"device set: {self.device}")
        self.config = GPT2Config(
                        vocab_size=self.vocab_size,
                        n_positions=self.n_positions,
                        n_ctx=self.n_ctx,
                        n_embd=self.n_embd,
                        n_layer=self.n_layer,
                        n_head=self.n_head
                    )
        print(f"Vocab size: {self.config.vocab_size}, type: {type(self.config.vocab_size)}")
        print(f"Embedding dim: {self.config.n_embd}, type: {type(self.config.n_embd)}")
        self.model = GPT2LMHeadModel(self.config).to(device=self.device)
        print(f"device set: {self.device}")

    def tokenize(self, example):
        tokenized = self.tokenizer(
            example["text"],
            truncation=True,
            padding="max_length",
            max_length=128
        )
        tokenized["labels"] = tokenized["input_ids"].copy()
        return tokenized
    
    def train(self):
        tokenized_dataset = self.dataset.map(self.tokenize, batched=True)
        training_args = TrainingArguments(
            output_dir="./results",
            num_train_epochs=3,
            per_device_train_batch_size=4,
            per_device_eval_batch_size=4,
            logging_steps=10,
            save_steps=500,
            learning_rate=5e-4,
            weight_decay=0.01,
            logging_dir="none"
        )

        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=tokenized_dataset["train"]
        )
        trainer.train()
        print("training completed!!")

    def inference( self):
        text_gen = self.pipeline("text-generation", model=self.model, tokenizer=self.tokenizer)
        print(text_gen("The universe is", max_length=50))

if __name__ == "__main__":
    model_id = "gpt2"
    tokenizer_id = "distilgpt2"
    sml = SLMGPT2(model_id=model_id, tokenizer_id=tokenizer_id)
    sml.train()


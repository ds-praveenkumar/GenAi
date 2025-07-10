from unsloth import FastLanguageModel
import torch
from datasets import load_dataset
from trl import SFTTrainer
from transformers import TrainingArguments, DataCollatorForSeq2Seq
from unsloth import is_bfloat16_supported
from unsloth.chat_templates import train_on_responses_only
import gc

model, tokenizer = FastLanguageModel.from_pretrained(
    model_name = "unsloth/meta-Llama-3.1-8B-Instruct",
    max_seq_length = 2048,
    dtype = None,
    load_in_4bit = True,
)

#Importing the dataset
dataset = load_dataset('csv', data_files='/home/praveen/Desktop/git/GenAi/data/nlp-mental-health-conversations/train.csv')
dataset["train"][0]

instruction = """You are an experienced psychologist named Amelia. 
Be polite to the patient and answer all mental health-related queries.
"""
def format_chat_template(row):
    
    row_json = [{"role": "system", "content": instruction },
               {"role": "user", "content": row["Context"]},
               {"role": "assistant", "content": row["Response"]}]
    
    row["text"] = tokenizer.apply_chat_template(row_json, tokenize=False)
    return row

dataset = dataset["train"].map(
    format_chat_template,
    num_proc= 4,
)
print(dataset["text"][2])

dataset = dataset.train_test_split(test_size=0.1)

model = FastLanguageModel.get_peft_model(
    model,
    r = 16,
    target_modules = ["q_proj", "k_proj", "v_proj", "o_proj",
                      "gate_proj", "up_proj", "down_proj",],
    lora_alpha = 16,
    lora_dropout = 0,
    bias = "none", 
    
    use_gradient_checkpointing = "unsloth", 
    random_state = 3407,
    use_rslora = False,
    loftq_config = None,
)

trainer = SFTTrainer(
    model = model,
    tokenizer = tokenizer,
    train_dataset=dataset["train"],
    eval_dataset=dataset["test"],
    dataset_text_field = "text",
    max_seq_length = 2048,
    data_collator = DataCollatorForSeq2Seq(tokenizer = tokenizer),
    dataset_num_proc = 2,
    packing = False, # Can make training 5x faster for short sequences.
    args = TrainingArguments(
        per_device_train_batch_size=2,
        per_device_eval_batch_size=2,
        gradient_accumulation_steps=4,
        eval_strategy="steps",
        eval_steps=0.2,
        warmup_steps = 5,
        # num_train_epochs = 1, # Set this for 1 full training run.
        max_steps = 60,
        learning_rate = 2e-4,
        fp16 = not is_bfloat16_supported(),
        bf16 = is_bfloat16_supported(),
        optim = "adamw_8bit",
        weight_decay = 0.01,
        lr_scheduler_type = "linear",
        seed = 3407,
        output_dir = "model_traning_outputs",
        report_to = "none",
    ),
)


trainer = train_on_responses_only(
    trainer,
    instruction_part = "<|start_header_id|>user<|end_header_id|>\n\n",
    response_part = "<|start_header_id|>assistant<|end_header_id|>\n\n",
)
torch.cuda.empty_cache()
gc.collect()

trainer_stats = trainer.train()

FastLanguageModel.for_inference(model)

messages = [{"role": "system", "content": instruction},
    {"role": "user", "content": "I don't have the will to live anymore. I don't feel happiness in anything. "}]

prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    
inputs = tokenizer(prompt, return_tensors='pt', padding=True, truncation=True).to("cuda")

outputs = model.generate(**inputs, max_new_tokens=150, num_return_sequences=1)

text = tokenizer.decode(outputs[0], skip_special_tokens=True)

print(text.split("assistant")[1])

new_model = "Llama-3.2-3b-it-mental-health"
model.save_pretrained(new_model)
tokenizer.save_pretrained(new_model)

print("training completed successfull!!")
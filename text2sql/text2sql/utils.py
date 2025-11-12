# sql_generator/utils.py
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

model_name = "defog/sqlcoder-7b-2"
model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto", torch_dtype=torch.float16)
tokenizer = AutoTokenizer.from_pretrained(model_name)
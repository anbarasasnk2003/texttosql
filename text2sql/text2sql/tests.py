  # In tests.py
from .utils import model, tokenizer

def test_model_generation(self):
    prompt = "Schema: Table users (id INT). Question: Show all users. SQL:"
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    outputs = model.generate(**inputs, max_new_tokens=50, do_sample=False)
    sql = tokenizer.decode(outputs[0], skip_special_tokens=True).split("SQL:")[-1].strip()
    self.assertTrue(sql.startswith("SELECT"))
  
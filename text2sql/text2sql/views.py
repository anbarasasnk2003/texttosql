import requests
from django.shortcuts import render

DEFOG_API_KEY = "759f5701f02bd85095b3a7de15ea6cec91e703e18d6868a0c728d0d09130f6c1"
DEFOG_URL = "https://api.defog.ai/generate_query_chat"  # example
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import re
from .utils import model, tokenizer

@csrf_exempt  # For simplicity; use CSRF tokens in production
def generate_sql(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        schema = data.get('schema', [])  # List of tables
        request_text = data.get('request', '')
        
        # Build schema string
        schema_str = ""
        for table in schema:
            cols = ", ".join([f"{col['name']} {col['type']}" for col in table['columns']])
            schema_str += f"Table {table['table']} ({cols}). "
        
        # Prompt
        prompt = f"Schema: {schema_str}\nQuestion: {request_text}\nSQL:"
        
        # Generate
        inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
        outputs = model.generate(**inputs, max_new_tokens=100, do_sample=False, temperature=0)
        full_output = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Extract SQL only
        sql_match = re.search(r'SQL:\s*(.*?);', full_output, re.DOTALL)
        sql_query = sql_match.group(1).strip() + ";" if sql_match else "Error: Could not generate SQL"
        
        return JsonResponse({'sql': sql_query})
    return JsonResponse({'error': 'Invalid request'}, status=400)

'''from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json, re
from .utils import model, tokenizer
@csrf_exempt
def generate_sql(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            schema = data.get('schema', [])
            request_text = data.get('request', '')
            
            # Build schema string
            schema_str = ""
            for table in schema:
                cols = ", ".join([f"{col['name']} {col['type']}" for col in table['columns']])
                schema_str += f"Table {table['table']} ({cols}). "
            
            # Prompt
            prompt = f"Schema: {schema_str}\nQuestion: {request_text}\nSQL:"
            
            # Generate
            inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
            outputs = model.generate(**inputs, max_new_tokens=100, do_sample=False)
            full_output = tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Extract SQL
            sql_match = re.search(r'SQL:\s*(.*?);', full_output, re.DOTALL)
            sql_query = sql_match.group(1).strip() + ";" if sql_match else "Error: Could not generate SQL"
            
            return JsonResponse({'sql': sql_query})
        except Exception as e:
            print(f"Error in generate_sql: {e}")  # Log to console
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request'}, status=400)
    # Generate SQL
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    outputs = model.generate(**inputs, max_new_tokens=100, do_sample=False, temperature=0)
    full_output = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # Extract SQL safely
    sql_match = re.search(r'SQL:\s*(.*)', full_output, re.DOTALL)
    sql_query = sql_match.group(1).strip() if sql_match else full_output.strip()

    return JsonResponse({'sql': sql_query})'''
'''
# views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import re
from .utils import model, tokenizer  # your HF model and tokenizer

@csrf_exempt  # for simplicity
def generate_sql(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request, POST required'}, status=400)

    try:
        data = json.loads(request.body)
        schema = data.get('schema', [])
        request_text = data.get('request', '')

        # Build schema string
        schema_str = ""
        for table in schema:
            cols = ", ".join([f"{col['name']} {col['type']}" for col in table['columns']])
            schema_str += f"Table {table['table']} ({cols}). "

        # Prompt for model
        prompt = f"Schema: {schema_str}\nQuestion: {request_text}\nSQL:"

        # Tokenize and generate
        inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
        outputs = model.generate(
            **inputs,
            max_new_tokens=100,
            do_sample=False,
            pad_token_id=model.config.eos_token_id  # removes warnings
        )
        full_output = tokenizer.decode(outputs[0], skip_special_tokens=True)

        # Extract SQL only
        sql_match = re.search(r'SQL:\s*(.*?);', full_output, re.DOTALL)
        sql_query = sql_match.group(1).strip() + ";" if sql_match else full_output.strip()

        return JsonResponse({'sql': sql_query})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)'''
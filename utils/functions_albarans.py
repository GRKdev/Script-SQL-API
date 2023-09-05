import json
import random
from querys.albaranes.query_albarans import ALBARAN_QUERIES, FACTURAS_QUERIES, PEDIDOS_QUERIES, ALB_CLIENT_DETAIL

def generate_random_prompts(train_count=100, valid_count=20, min_value=1, max_value=10000):
    train_prompts = [str(random.randint(min_value, max_value)) for _ in range(train_count)]
    valid_prompts = [str(random.randint(min_value, max_value)) for _ in range(valid_count)]
    return train_prompts, valid_prompts

def generate_url_query(table_name, function_name, prompt):
    prompt_components = ','.join(prompt.split())
    return f"/api/{table_name}?{function_name}={prompt_components}&&"


def generate_url_query_albaran(table_name, function_name, prompt):
    prompt_components = ','.join(prompt.split())
    return f"/api/alb/{table_name}?{function_name}={prompt_components}&&"

def generate_url_query_detail(table_name, function_name, prompt):
    prompt_components = ','.join(prompt.split())
    return f"/api/alb/{table_name}?{function_name}={prompt_components}&&"



def generate_albaran_all(generated_lines, table_name, function_name, prompts_list):
    for idx, prompt in enumerate(prompts_list):
        query_format = ALBARAN_QUERIES[idx % len(ALBARAN_QUERIES)]
        prompt_text = query_format.format(prompt=prompt)
        query = generate_url_query_albaran(table_name, function_name, prompt)
        line = {
            "prompt": prompt_text,
            "completion": query
        }
        generated_lines.append(json.dumps(line, ensure_ascii=False))

def generate_albaran_detalle_cliente(generated_lines, table_name, function_name, prompts_list):
    for idx, prompt in enumerate(prompts_list):
        query_format = ALB_CLIENT_DETAIL[idx % len(ALB_CLIENT_DETAIL)]
        prompt_text = query_format.format(prompt=prompt)
        query = generate_url_query_detail(table_name, function_name, prompt)
        line = {
            "prompt": prompt_text,
            "completion": query
        }
        generated_lines.append(json.dumps(line, ensure_ascii=False))

def generate_facturas_queries(generated_lines, table_name, function_name, prompts_list):
    for idx, prompt in enumerate(prompts_list):
        query_format = FACTURAS_QUERIES[idx % len(FACTURAS_QUERIES)]
        prompt_text = query_format.format(prompt=prompt)
        query = generate_url_query(table_name, function_name, prompt)
        line = {
            "prompt": prompt_text,
            "completion": query
        }
        generated_lines.append(json.dumps(line, ensure_ascii=False))

def generate_pedidos_queries(generated_lines, table_name, function_name, prompts_list):
    for idx, prompt in enumerate(prompts_list):
        query_format = PEDIDOS_QUERIES[idx % len(PEDIDOS_QUERIES)]
        prompt_text = query_format.format(prompt=prompt)
        query = generate_url_query(table_name, function_name, prompt)
        line = {
            "prompt": prompt_text,
            "completion": query
        }
        generated_lines.append(json.dumps(line, ensure_ascii=False))

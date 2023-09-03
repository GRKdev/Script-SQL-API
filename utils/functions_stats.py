import json
import random
from querys.stats.query_facturacio_stats import FACT_ANUALES_Q, FACT_CY_Q, FACT_MULTIPLE_Q, FACT_SELECTY_Q

def generate_random_prompts(train_count=100, valid_count=20, min_value=1, max_value=10000):
    train_prompts = [str(random.randint(min_value, max_value)) for _ in range(train_count)]
    valid_prompts = [str(random.randint(min_value, max_value)) for _ in range(valid_count)]
    return train_prompts, valid_prompts

def generate_url_query(table_name, function_name, prompt):
    prompt_components = ','.join(prompt.split())
    return f"/api/{table_name}?{function_name}={prompt_components}&&"

def generate_url_query_total(table_name):
    return f"/api/{table_name}?total=true&&"

def generate_fact_anuales(generated_lines, table_name):
    for idx, prompt in enumerate(prompts_list):
        query_format = FACT_ANUALES_Q[idx % len(FACT_ANUALES_Q)]
        prompt_text = query_format.format(prompt=prompt)
        query = generate_url_query(table_name)
        line = {
            "completion": query
        }
        generated_lines.append(json.dumps(line, ensure_ascii=False))

def generate_albaran_queries(generated_lines, table_name, function_name, prompts_list):
    for idx, prompt in enumerate(prompts_list):
        query_format = FACT_ANUALES_Q[idx % len(FACT_ANUALES_Q)]
        prompt_text = query_format.format(prompt=prompt)
        query = generate_url_query(table_name, function_name, prompt)
        line = {
            "prompt": prompt_text,
            "completion": query
        }
        generated_lines.append(json.dumps(line, ensure_ascii=False))        
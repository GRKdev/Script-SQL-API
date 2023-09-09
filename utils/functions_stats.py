import json
import random
from querys.stats.query_facturacio_stats import (
    FACT_ANUALES_Q, FACT_CURRENT_YEAR, FACT_SELECTED_YEAR,
    GANANCIAS_ANUALES, GANANCIAS_ANO_ACTUAL, GANANCIAS_SELECTED_YEAR
    )
from querys.stats.query_clients_stats import (
    FACT_CURRENT_YEAR_CLIENTES, FACT_ANUALES_CLIENTES,
    GANANCIAS_CURRENT_YEAR_CLIENTES, GANANCIAS_TOTALES_CLIENTES
    )

def filter_prompt(prompt):
    words = prompt.split()
    exact_exclusions = ["de", "el", "la", "dels", "els", "las", "i", "y", "los", "l'", "d'"]
    start_exclusions = ["d'", "l'"]
    filtered_words = []

    for i, word in enumerate(words):
        clean_word = word
        for excl in start_exclusions:
            if clean_word.lower().startswith(excl) and len(clean_word) > len(excl):
                clean_word = clean_word.replace(excl, "", 1)
        if clean_word.lower() in [e.lower() for e in exact_exclusions]:
            if i == 0 or i == len(words) - 1 or words[i - 1].lower() in [e.lower() for e in exact_exclusions] or words[i + 1].lower() in [e.lower() for e in exact_exclusions]:
                clean_word = ""
            else:
                continue
        if clean_word:
            filtered_words.append(clean_word.strip())
    
    return ' '.join(filtered_words)


def generate_random_years(train_count=100, valid_count=20):
    train_prompts = [str(random.randint(1999, 2030)) for _ in range(train_count)]
    valid_prompts = [str(random.randint(1999, 2030)) for _ in range(valid_count)]
    return train_prompts, valid_prompts


def load_names_from_json(filename="Documents/dicc/clientes/clientes_general.json"):
    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)
        return data
    
def generate_url_query_prueba(table_name, function_name, *prompts):
    prompt_components = []
    for idx, prompt in enumerate(prompts):
        clean_prompt = ','.join(filter_prompt(prompt).split())
        suffix = str(idx + 1) if idx > 0 else ''
        prompt_components.append(f"{function_name}{suffix}={clean_prompt}")
    prompt_string = '&'.join(prompt_components)
    return f"api/{table_name}?{prompt_string}&&"

def generate_url_query(table_name, function_name, prompt):
    prompt_components = ','.join(prompt.split())
    return f"/api/{table_name}?{function_name}={prompt_components}&&"

def generate_url_query_total(table_name, function_name):
    return f"/api/{table_name}?{function_name}=true&&"

def generate_url_query_current_year(table_name, function_name):
    return f"/api/{table_name}?{function_name}=true&&"

def generate_url_query_selected_year(table_name, function_name, prompt):
    prompt_components = ','.join(prompt.split())
    return f"/api/{table_name}?{function_name}={prompt_components}&&"

def generate_url_query_total_ing(table_name, function_name):
    return f"/api/{table_name}?{function_name}=true&&"

def generate_url_query_current_year_ing(table_name, function_name):
    return f"/api/{table_name}?{function_name}=true&&"

def generate_url_query_selected_year_ing(table_name, function_name, prompt):
    prompt_components = ','.join(prompt.split())
    return f"/api/{table_name}?{function_name}={prompt_components}&&"

def generate_fact_current_year_client(generated_lines, table_name, function_name, prompts_list):
    for idx, prompt in enumerate(prompts_list):
        query_format = FACT_CURRENT_YEAR_CLIENTES[idx % len(FACT_CURRENT_YEAR_CLIENTES)]
        prompt_text = query_format.format(prompt=prompt)
        query = generate_url_query(table_name, function_name, prompt)
        line = {
            "prompt": prompt_text,
            "completion": query
        }
        generated_lines.append(json.dumps(line, ensure_ascii=False))        

def generate_fact_total_client(generated_lines, table_name, function_name, prompts_list):
    for idx, prompt in enumerate(prompts_list):
        query_format = FACT_ANUALES_CLIENTES[idx % len(FACT_ANUALES_CLIENTES)]
        prompt_text = query_format.format(prompt=prompt)
        query = generate_url_query_prueba(table_name, function_name, prompt)
        line = {
            "prompt": prompt_text,
            "completion": query
        }
        generated_lines.append(json.dumps(line, ensure_ascii=False))        

def generate_ing_current_year_client(generated_lines, table_name, function_name, prompts_list):
    for idx, prompt in enumerate(prompts_list):
        query_format = GANANCIAS_CURRENT_YEAR_CLIENTES[idx % len(GANANCIAS_CURRENT_YEAR_CLIENTES)]
        prompt_text = query_format.format(prompt=prompt)
        query = generate_url_query(table_name, function_name, prompt)
        line = {
            "prompt": prompt_text,
            "completion": query
        }
        generated_lines.append(json.dumps(line, ensure_ascii=False))        

def generate_ing_total_client(generated_lines, table_name, function_name, prompts_list):
    for idx, prompt in enumerate(prompts_list):
        query_format = GANANCIAS_TOTALES_CLIENTES[idx % len(GANANCIAS_TOTALES_CLIENTES)]
        prompt_text = query_format.format(prompt=prompt)
        query = generate_url_query(table_name, function_name, prompt)
        line = {
            "prompt": prompt_text,
            "completion": query
        }
        generated_lines.append(json.dumps(line, ensure_ascii=False))        

def generate_fact_total(generated_lines, table_name, function_name, prompts_list):
    for idx, prompt in enumerate(prompts_list):
        query_format = FACT_ANUALES_Q[idx % len(FACT_ANUALES_Q)]
        prompt_text = query_format.format(prompt=prompt)
        query = generate_url_query_total(table_name, function_name)
        line = {
            "prompt": prompt_text,
            "completion": query
        }
        generated_lines.append(json.dumps(line, ensure_ascii=False))

def generate_fact_current_year(generated_lines, table_name, function_name, prompts_list):
    for idx, prompt in enumerate(prompts_list):
        query_format = FACT_CURRENT_YEAR[idx % len(FACT_CURRENT_YEAR)]
        prompt_text = query_format.format(prompt=prompt)
        query = generate_url_query_current_year(table_name, function_name)
        line = {
            "prompt": prompt_text,
            "completion": query
        }
        generated_lines.append(json.dumps(line, ensure_ascii=False))

def generate_fact_selected_year(generated_lines, table_name, function_name, prompts_list):
    for idx, prompt in enumerate(prompts_list):
        query_format = FACT_SELECTED_YEAR[idx % len(FACT_SELECTED_YEAR)]
        prompt_text = query_format.format(prompt=prompt)
        query = generate_url_query_selected_year(table_name, function_name, prompt)
        line = {
            "prompt": prompt_text,
            "completion": query
        }
        generated_lines.append(json.dumps(line, ensure_ascii=False))

def generate_ing_total(generated_lines, table_name, function_name, prompts_list):
    for idx, prompt in enumerate(prompts_list):
        query_format = GANANCIAS_ANUALES[idx % len(GANANCIAS_ANUALES)]
        prompt_text = query_format.format(prompt=prompt)
        query = generate_url_query_total_ing(table_name, function_name)
        line = {
            "prompt": prompt_text,
            "completion": query
        }
        generated_lines.append(json.dumps(line, ensure_ascii=False))

def generate_ing_current_year(generated_lines, table_name, function_name, prompts_list):
    for idx, prompt in enumerate(prompts_list):
        query_format = GANANCIAS_ANO_ACTUAL[idx % len(GANANCIAS_ANO_ACTUAL)]
        prompt_text = query_format.format(prompt=prompt)
        query = generate_url_query_current_year_ing(table_name, function_name)
        line = {
            "prompt": prompt_text,
            "completion": query
        }
        generated_lines.append(json.dumps(line, ensure_ascii=False))

def generate_ing_selected_year(generated_lines, table_name, function_name, prompts_list):
    for idx, prompt in enumerate(prompts_list):
        query_format = GANANCIAS_SELECTED_YEAR[idx % len(GANANCIAS_SELECTED_YEAR)]
        prompt_text = query_format.format(prompt=prompt)
        query = generate_url_query_selected_year_ing(table_name, function_name, prompt)
        line = {
            "prompt": prompt_text,
            "completion": query
        }
        generated_lines.append(json.dumps(line, ensure_ascii=False))
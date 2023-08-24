import json
from querys.articulos.query_articulos import ARTICULOS_QUERIES, PROVEEDOR_QUERIES
import random

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
            # Verifica si está rodeado por espacios o al principio/final
            if i == 0 or i == len(words) - 1 or words[i - 1].lower() in [e.lower() for e in exact_exclusions] or words[i + 1].lower() in [e.lower() for e in exact_exclusions]:
                clean_word = ""
            else:
                continue
        if clean_word:
            filtered_words.append(clean_word.strip())
    
    return ' '.join(filtered_words)

def generate_like_conditions(column_name, prompt):
    cleaned_prompt = filter_prompt(prompt)
    conditions = [f"{column_name} LIKE '%{word}%'" for word in cleaned_prompt.split()]
    return " AND ".join(conditions)

def generate_random_prompts(train_count=100, valid_count=20, min_value=1, max_value=2000):
    train_prompts = [str(random.randint(min_value, max_value)) for _ in range(train_count)]
    valid_prompts = [str(random.randint(min_value, max_value)) for _ in range(valid_count)]
    return train_prompts, valid_prompts


def load_prompts_from_json(filename="Documents/dicc/articulos/articulos_general.json"):
    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)
        return data

def generate_url_query(table_name, function_name, prompt):
    cleaned_prompt = filter_prompt(prompt)
    prompt_components = ','.join(cleaned_prompt.split())  # Convert spaces to commas
    return f"/api/{table_name}?{function_name}={prompt_components}&&"

def generate_custom_queries(generated_lines, table_name, function_name, prompts_list):
    for idx, prompt in enumerate(prompts_list):
        query_format = ARTICULOS_QUERIES[idx % len(ARTICULOS_QUERIES)]
        prompt_text = query_format.format(prompt=prompt)
        query = generate_url_query(table_name, function_name, prompt)
        line = {
            "prompt": prompt_text,
            "completion": query
        }
        generated_lines.append(json.dumps(line, ensure_ascii=False))

def generate_proveedores_queries(generated_lines, table_name, function_name, prompts_list):
    for idx, prompt in enumerate(prompts_list):
        query_format = PROVEEDOR_QUERIES[idx % len(PROVEEDOR_QUERIES)]
        prompt_text = query_format.format(prompt=prompt)
        query = generate_url_query(table_name, function_name, prompt)
        line = {
            "prompt": prompt_text,
            "completion": query
        }
        generated_lines.append(json.dumps(line, ensure_ascii=False))

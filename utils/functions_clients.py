import json
from querys.clients.query_clients import CLIENT_QUERIES, TELEFON_QUERIES, EMAIL_QUERIES, DIRECCIO_QUERIES, CLIENT_MULTI_QUERIES, TELEFON_QUERIES_MULTIPLE, EMAIL_QUERIES_MULTIPLE, DIRECCIO_QUERIES_MULTIPLE

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


def load_names_from_json(filename="Documents/dicc/clientes/clientes_general.json"):
    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)
        return data

def generate_url_query(table_name, function_name, *prompts):
    prompt_components = []
    for idx, prompt in enumerate(prompts):
        clean_prompt = ','.join(filter_prompt(prompt).split())
        suffix = str(idx + 1) if idx > 0 else ''
        prompt_components.append(f"{function_name}{suffix}={clean_prompt}")
    prompt_string = '&'.join(prompt_components)
    return f"api/{table_name}?{prompt_string}&&"


def generate_custom_queries(generated_lines, table_name, function_name, prompts_list):
    for idx, prompt in enumerate(prompts_list):
        query_format = CLIENT_QUERIES[idx % len(CLIENT_QUERIES)]
        prompt_text = query_format.format(prompt=prompt)
        query = generate_url_query(table_name, function_name, prompt)
        line = {
            "prompt": prompt_text,
            "completion": query
        }
        generated_lines.append(json.dumps(line, ensure_ascii=False))

def generate_telefon_queries(generated_lines, table_name, function_name, prompts_list):
    for idx, prompt in enumerate(prompts_list):
        query_format = TELEFON_QUERIES[idx % len(TELEFON_QUERIES)]
        prompt_text = query_format.format(prompt=prompt)
        query = generate_url_query(table_name, function_name, prompt)
        line = {
            "prompt": prompt_text,
            "completion": query
        }
        generated_lines.append(json.dumps(line, ensure_ascii=False))

def generate_email_queries(generated_lines, table_name, function_name, prompts_list):
    for idx, prompt in enumerate(prompts_list):
        query_format = EMAIL_QUERIES[idx % len(EMAIL_QUERIES)]
        prompt_text = query_format.format(prompt=prompt)
        query = generate_url_query(table_name, function_name, prompt)
        line = {
            "prompt": prompt_text,
            "completion": query
        }
        generated_lines.append(json.dumps(line, ensure_ascii=False))

def generate_direccio_queries(generated_lines, table_name, function_name, prompts_list):
    for idx, prompt in enumerate(prompts_list):
        query_format = DIRECCIO_QUERIES[idx % len(DIRECCIO_QUERIES)]
        prompt_text = query_format.format(prompt=prompt)
        query = generate_url_query(table_name, function_name, prompt)
        line = {
            "prompt": prompt_text,
            "completion": query
        }
        generated_lines.append(json.dumps(line, ensure_ascii=False))

def generate_custom_queries_multi(generated_lines, table_name, function_name, prompts_list):
    for idx in range(0, len(prompts_list), 2):
        if idx + 1 < len(prompts_list):
            query_format = CLIENT_MULTI_QUERIES[idx % len(CLIENT_MULTI_QUERIES)]
            prompt1, prompt2 = prompts_list[idx], prompts_list[idx + 1]
            prompt_text = query_format.format(prompt1=prompt1, prompt2=prompt2)
            query = generate_url_query(table_name, function_name, prompt1, prompt2)
            line = {
                "prompt": prompt_text,
                "completion": query
            }
            generated_lines.append(json.dumps(line, ensure_ascii=False))

def generate_telefon_multi(generated_lines, table_name, function_name, prompts_list):
    for idx in range(0, len(prompts_list), 2):
        if idx + 1 < len(prompts_list):
            query_format = TELEFON_QUERIES_MULTIPLE[idx % len(TELEFON_QUERIES_MULTIPLE)]
            prompt1, prompt2 = prompts_list[idx], prompts_list[idx + 1]
            prompt_text = query_format.format(prompt1=prompt1, prompt2=prompt2)
            query = generate_url_query(table_name, function_name, prompt1, prompt2)
            line = {
                "prompt": prompt_text,
                "completion": query
            }
            generated_lines.append(json.dumps(line, ensure_ascii=False))

def generate_email_multi(generated_lines, table_name, function_name, prompts_list):
    for idx in range(0, len(prompts_list), 2):
        if idx + 1 < len(prompts_list):
            query_format = EMAIL_QUERIES_MULTIPLE[idx % len(EMAIL_QUERIES_MULTIPLE)]
            prompt1, prompt2 = prompts_list[idx], prompts_list[idx + 1]
            prompt_text = query_format.format(prompt1=prompt1, prompt2=prompt2)
            query = generate_url_query(table_name, function_name, prompt1, prompt2)
            line = {
                "prompt": prompt_text,
                "completion": query
            }
            generated_lines.append(json.dumps(line, ensure_ascii=False))       

def generate_direc_multi(generated_lines, table_name, function_name, prompts_list):
    for idx in range(0, len(prompts_list), 2):
        if idx + 1 < len(prompts_list): 
            query_format = DIRECCIO_QUERIES_MULTIPLE[idx % len(DIRECCIO_QUERIES_MULTIPLE)]
            prompt1, prompt2 = prompts_list[idx], prompts_list[idx + 1]
            prompt_text = query_format.format(prompt1=prompt1, prompt2=prompt2)
            query = generate_url_query(table_name, function_name, prompt1, prompt2)
            line = {
                "prompt": prompt_text,
                "completion": query
            }
            generated_lines.append(json.dumps(line, ensure_ascii=False))            
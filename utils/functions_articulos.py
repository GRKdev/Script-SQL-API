import json
from querys.articulos.query_articulos import (
    ARTICULOS_QUERIES,
    PROVEEDOR_QUERIES,
    PRECIO_ARTICULOS_QUERIES_COSTE,
    PRECIO_ARTICULOS_QUERIES_VENTA,
    ARTICULOS_COMPLETOS_QUERIES,
)
import random


def filter_prompt(prompt):
    words = prompt.split()
    exact_exclusions = [
        "de",
        "el",
        "la",
        "dels",
        "els",
        "las",
        "i",
        "y",
        "los",
        "l'",
        "d'",
    ]
    start_exclusions = ["d'", "l'"]
    filtered_words = []
    for i, word in enumerate(words):
        clean_word = word
        for excl in start_exclusions:
            if clean_word.lower().startswith(excl) and len(clean_word) > len(excl):
                clean_word = clean_word.replace(excl, "", 1)

        if clean_word.lower() in [e.lower() for e in exact_exclusions]:
            if (
                i == 0
                or i == len(words) - 1
                or words[i - 1].lower() in [e.lower() for e in exact_exclusions]
                or words[i + 1].lower() in [e.lower() for e in exact_exclusions]
            ):
                clean_word = ""
            else:
                continue
        if clean_word:
            filtered_words.append(clean_word.strip())
    return " ".join(filtered_words)


def generate_random_numbers(
    train_count=100, valid_count=20, min_value=1, max_value=2000
):
    train_prompts = [
        str(random.randint(min_value, max_value)) for _ in range(train_count)
    ]
    valid_prompts = [
        str(random.randint(min_value, max_value)) for _ in range(valid_count)
    ]
    return train_prompts, valid_prompts


def generate_random_bars(train_count=100, valid_count=20):
    half_train = train_count // 2
    half_valid = valid_count // 2

    segment_size_train = half_train // 9 if half_train // 9 != 0 else 1
    segment_size_valid = half_valid // 9 if half_valid // 9 != 0 else 1

    train_12_digits = [
        str(i) + str(random.randint(10 ** (10), 10 ** (11) - 1))
        for i in range(1, 10)
        for _ in range(segment_size_train)
    ]
    valid_12_digits = [
        str(i) + str(random.randint(10 ** (10), 10 ** (11) - 1))
        for i in range(1, 10)
        for _ in range(segment_size_valid)
    ]

    train_13_digits = [
        str(i) + str(random.randint(10 ** (11), 10 ** (12) - 1))
        for i in range(1, 10)
        for _ in range(segment_size_train)
    ]
    valid_13_digits = [
        str(i) + str(random.randint(10 ** (11), 10 ** (12) - 1))
        for i in range(1, 10)
        for _ in range(segment_size_valid)
    ]

    train_prompts = train_12_digits + train_13_digits
    valid_prompts = valid_12_digits + valid_13_digits

    while len(train_prompts) < train_count:
        train_prompts.append(
            str(random.randint(1, 9)) + str(random.randint(10 ** (10), 10 ** (12) - 1))
        )

    while len(valid_prompts) < valid_count:
        valid_prompts.append(
            str(random.randint(1, 9)) + str(random.randint(10 ** (10), 10 ** (12) - 1))
        )

    random.shuffle(train_prompts)
    random.shuffle(valid_prompts)

    return train_prompts, valid_prompts


def load_prompts_from_json(filename="Documents/dicc/articulos/articulos_general.json"):
    with open(filename, "r", encoding="utf-8") as file:
        data = json.load(file)
        return data


def generate_url_query(table_name, function_name, prompt):
    cleaned_prompt = filter_prompt(prompt)
    prompt_components = ",".join(cleaned_prompt.split())
    return f"/api/{table_name}?{function_name}={prompt_components}&&"


def generate_custom_queries(
    generated_lines, table_name, function_name, prompts_list, is_valid=False
):
    for idx, prompt in enumerate(prompts_list):
        query_format = (
            random.choice(ARTICULOS_QUERIES)
            if is_valid
            else ARTICULOS_QUERIES[idx % len(ARTICULOS_QUERIES)]
        )
        prompt_text = query_format.format(prompt=prompt)
        query = generate_url_query(table_name, function_name, prompt.lower())
        line = {"prompt": prompt_text, "completion": query}
        generated_lines.append(json.dumps(line, ensure_ascii=False))


def generate_proveedores_queries(
    generated_lines, table_name, function_name, prompts_list, is_valid=False
):
    for idx, prompt in enumerate(prompts_list):
        query_format = (
            random.choice(PROVEEDOR_QUERIES)
            if is_valid
            else PROVEEDOR_QUERIES[idx % len(PROVEEDOR_QUERIES)]
        )
        prompt_text = query_format.format(prompt=prompt)
        query = generate_url_query(table_name, function_name, prompt.lower())
        line = {"prompt": prompt_text, "completion": query}
        generated_lines.append(json.dumps(line, ensure_ascii=False))


def generate_precioart_queries_coste(
    generated_lines, table_name, function_name, prompts_list, is_valid=False
):
    for idx, prompt in enumerate(prompts_list):
        query_format = (
            random.choice(PRECIO_ARTICULOS_QUERIES_COSTE)
            if is_valid
            else PRECIO_ARTICULOS_QUERIES_COSTE[
                idx % len(PRECIO_ARTICULOS_QUERIES_COSTE)
            ]
        )
        prompt_text = query_format.format(prompt=prompt)
        query = generate_url_query(table_name, function_name, prompt.lower())
        line = {"prompt": prompt_text, "completion": query}
        generated_lines.append(json.dumps(line, ensure_ascii=False))


def generate_precioart_queries_venta(
    generated_lines, table_name, function_name, prompts_list, is_valid=False
):
    for idx, prompt in enumerate(prompts_list):
        query_format = (
            random.choice(PRECIO_ARTICULOS_QUERIES_VENTA)
            if is_valid
            else PRECIO_ARTICULOS_QUERIES_VENTA[
                idx % len(PRECIO_ARTICULOS_QUERIES_VENTA)
            ]
        )
        prompt_text = query_format.format(prompt=prompt)
        query = generate_url_query(table_name, function_name, prompt.lower())
        line = {"prompt": prompt_text, "completion": query}
        generated_lines.append(json.dumps(line, ensure_ascii=False))


def generate_codebar_queries(generated_lines, table_name, function_name, prompts_list):
    for prompt in prompts_list:
        query = f"/api/{table_name}?{function_name}={prompt}&&"
        line = {"prompt": prompt, "completion": query}
        generated_lines.append(json.dumps(line, ensure_ascii=False))


def generate_toda_la_info(
    generated_lines, table_name, function_name, prompts_list, is_valid=False
):
    for idx, prompt in enumerate(prompts_list):
        query_format = (
            random.choice(ARTICULOS_COMPLETOS_QUERIES)
            if is_valid
            else ARTICULOS_COMPLETOS_QUERIES[idx % len(ARTICULOS_COMPLETOS_QUERIES)]
        )
        prompt_text = query_format.format(prompt=prompt)
        query = generate_url_query(table_name, function_name, prompt.lower())
        line = {"prompt": prompt_text, "completion": query}
        generated_lines.append(json.dumps(line, ensure_ascii=False))

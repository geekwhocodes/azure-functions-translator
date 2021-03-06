from transformers import T5Tokenizer, T5ForConditionalGeneration
from time import time
import os
import logging

models_dir_name = "models"

# TODO: Refactor
az_file_share_mount_path = "/models"
# Temp var
on_azure_key = "ON_AZURE"


def get_model_path(function_directory):
    on_azure = os.getenv(on_azure_key)
    logging.info(f"onzure - {on_azure}")
    model_name = os.getenv("CURRENT_MODEL", "t5-small")
    if function_directory and not on_azure:
        root_path = os.path.dirname(function_directory)
        module_path = os.path.join(root_path, models_dir_name, model_name)
        return module_path
    else:
        if on_azure:
            model_path = os.path.join(az_file_share_mount_path, model_name)
            print(f"Computed model path - {model_path}")
            return model_path
        else:
            ValueError("Models directory not found")


def summarize(function_directory, text):
    model_path = get_model_path(function_directory)
    logging.info(f"Loading model from {model_path}")
    start = time()
    tokenizer = T5Tokenizer.from_pretrained(model_path)
    model = T5ForConditionalGeneration.from_pretrained(model_path)
    logging.info(f"Model loaded in {round(time()-start, 2)}s.")

    logging.info("Tokenizing data...")
    input_text = tokenizer.encode(f"summarize: :{text}", return_tensors="pt")
    start = time()
    translated = model.generate(input_text)
    logging.info(f"Model executed in {round(time()-start, 2)}s.")

    logging.info("Generating result...")
    start = time()
    result = tokenizer.decode(translated[0], skip_special_tokens=True)
    logging.info(f"Result generated in {round(time()-start, 2)}s.")
    return result

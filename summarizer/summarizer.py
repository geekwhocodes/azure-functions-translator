from transformers import T5Tokenizer, T5ForConditionalGeneration
from time import time
import os

models_dir_name = "models"
model_name = "t5-small"


def summarize(function_directory, text):
    root_path = os.path.dirname(function_directory)
    module_path = os.path.join(root_path, models_dir_name, model_name)
    print(f"Loading model from {module_path}")
    start = time()
    tokenizer = T5Tokenizer.from_pretrained(module_path)
    model = T5ForConditionalGeneration.from_pretrained(module_path)
    print(f"Model loaded in {round(time()-start, 2)}s.")

    print("Tokenizing data...")
    input_text = tokenizer.encode(f"summarize: :{text}", return_tensors="pt")
    start = time()
    translated = model.generate(input_text)
    print(f"Model executed in {round(time()-start, 2)}s.")

    print("Generating result...")
    start = time()
    result = tokenizer.decode(translated[0], skip_special_tokens=True)
    print(f"Result generated in {round(time()-start, 2)}s.")
    return result

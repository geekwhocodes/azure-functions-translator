import os
import logging
import json
import azure.functions as func
from ..shared.summarizer import summarize


def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    logging.info("Python HTTP trigger function processed a request.")
    # os.environ["WEBSITE_INSTANCE_ID"] = "l;jd"
    try:
        req_body = req.get_json()
        if not req_body:
            return func.HttpResponse("Request body not valid", status_code=400)
        else:
            text = req_body.get("text")
            set_current_model(req_body.get("model"))
            if not text:
                return func.HttpResponse("Request body not valid", status_code=400)
            else:
                # TODO Add null check
                result = summarize(context.function_directory, text)
                data = {"translatedText": result}
                return func.HttpResponse(json.dumps(data), status_code=200)
    except ValueError:
        return func.HttpResponse("Something went wrong", status_code=500)


def set_current_model(model):
    if model:
        os.environ["CURRENT_MODEL"] = model
    else:
        os.environ["CURRENT_MODEL"] = "t5-small"

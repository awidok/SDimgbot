def extract_parameter(text, name, type, default=None):
    prefix = "--{}=".format(name)
    if prefix in text:
        value = text[text.find(prefix) + len(prefix):].split(" ")[0]
        if len(value) == 0:
            return default, text
        try:
            return type(value), text.replace(prefix+value, "").strip()
        except:
            return default, text
    else:
        return default, text


def split_prompts(text):
    result = text.split("--neg--")
    if len(result) < 2:
        return text, ""
    return result[0], result[1]

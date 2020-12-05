
from pathlib import Path
from typing import List, Optional, Tuple, overload
from pydantic import BaseModel
from transformers.models.gpt2 import GPT2LMHeadModel
from transformers.models.gpt2 import GPT2TokenizerFast

import os
# import gdown

# model_url = os.environ.get('MODEL_URL')
# config_url = os.environ.get('CONFIG_URL')


model_path = Path('model/pytorch_model.bin')
config_path = Path('model/config.json')
vocab_path = Path('model/encoder.json')
merges_path = Path('model/vocab.bpe')

# if not model_path.exists():
#     gdown.download(model_url, str(model_path.resolve()), quiet=False)

# if not config_path.exists():
#     gdown.download(config_url, str(config_path.resolve()), quiet=False)

print('Loading model...')
model = GPT2LMHeadModel.from_pretrained(
    str(model_path), config=str(config_path))
print('Model loaded.')

tokenizer = GPT2TokenizerFast(vocab_file=str(
    vocab_path), merges_file=str(merges_path))


class ModelOut(BaseModel):
    prompt: str
    output: str


def generate(prompt: str = '',
             top_k: int = 40,
             top_p: float = 0.95,
             temperature: float = 1.2,
             max_length: int = 256,
             min_length: int = 100,
             do_sample: bool = True,
             ) -> ModelOut:
    """
    Generate from a given prompt.

    If `prompt` is empty, or contains only whitespace, it will be set to '<|endoftext|>'.

    `max_length` – The maximum length of the sequence to be generated.

    `min_length` – The minimum length of the sequence to be generated.

    `temperature` – The value used to module the next token probabilities.

    `top_k` – The number of highest probability vocabulary tokens to keep for top-k-filtering.

    `top_p` – If set to float < 1, only the most probable tokens with probabilities that add up to top_p or higher are kept for generation.

    `do_sample` – If true, use sampling for text generation. Else use greedy search.

    Returns the given prompt and the output
    """
    if prompt.strip() == '':
        prompt = '<|endoftext|>'

    input_ids = tokenizer.encode(prompt, return_tensors='pt')

    # prevent an error from using a length greater than the model
    max_length = min(model.config.n_positions, max_length)

    outputs = model.generate(
        input_ids=input_ids,
        max_length=max_length,
        min_length=min_length,
        temperature=temperature,
        top_k=top_k,
        top_p=top_p,
        do_sample=do_sample,
    )

    return ModelOut(prompt=prompt, output=tokenizer.decode(outputs[0].detach().numpy(), skip_special_tokens=True).replace(prompt, '', 1))


def lstrip_play_id(text: str) -> str:
    return '\n'.join(line.split('|', maxsplit=1)[-1] for line in text.splitlines())


def generate_in_play(prompt: Optional[str], play_id: int = 6, remove_id: bool = True):
    if prompt is None:
        lines = ''
        raw_lines = ''
    else:
        raw_lines = prompt.splitlines()
        if play_id:
            lines = [f'{play_id}|{line}' for line in raw_lines]
        else:
            lines = raw_lines

        lines = '\n'.join(lines)

    output = generate(lines).output.replace(lines, '', 1)

    if remove_id:
        return ModelOut(prompt='\n'.join(raw_lines), output=lstrip_play_id(output))
        # return raw_prompt, lstrip_play_id(output)
    else:
        return ModelOut(prompt=lines, output=output)


if __name__ == "__main__":
    print(generate_in_play(
        prompt='Hamlet:\nTo be or not to be--that is the question:'))
    # print(generate('6|')[0])

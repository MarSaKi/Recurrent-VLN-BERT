import json
from pytorch_transformers import (BertConfig, BertTokenizer)
from tqdm import tqdm

def pad_instr_tokens(instr_tokens, maxlength=20):
    
    if len(instr_tokens) <= 2: #assert len(raw_instr_tokens) > 2
        return None

    if len(instr_tokens) > maxlength - 2: # -2 for [CLS] and [SEP]
        instr_tokens = instr_tokens[:(maxlength-2)]

    instr_tokens = ['[CLS]'] + instr_tokens + ['[SEP]']
    num_words = len(instr_tokens)  # - 1  # include [SEP]
    instr_tokens += ['[PAD]'] * (maxlength-len(instr_tokens))

    assert len(instr_tokens) == maxlength

    return instr_tokens, num_words

tokenizer_class = BertTokenizer
tokenizer = tokenizer_class.from_pretrained('bert-base-uncased')

with open('prepocess/ad_sep.json') as f:
    csz_data = json.load(f)

csz_data_new = []
for idx, item in tqdm(enumerate(csz_data)):
    instr = item['instructions'][0]
    instr_tokens = tokenizer.tokenize(instr)
    if len(instr_tokens) <= 2:
        continue
    padded_instr_tokens, num_words = pad_instr_tokens(instr_tokens, 80)
    item['instr_enc'] = tokenizer.convert_tokens_to_ids(padded_instr_tokens)
    csz_data_new.append(item)

print(len(csz_data), len(csz_data_new))
json.dump(
    csz_data_new,
    open('prepocess/ad_sep_tok.json', 'w'),
    sort_keys=True, indent=4, separators=(',', ': ')
)

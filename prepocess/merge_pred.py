import json
from tqdm import tqdm

fns = ['prepocess/argmax_seed_1',
       'prepocess/sample_seed_2',
       'prepocess/sample_seed_3',
       'prepocess/sample_seed_4',
       'prepocess/sample_seed_5',
       'prepocess/sample_seed_6',]

with open('prepocess/total_merged_origin.json') as f:
       origin_merge = json.load(f)

# origin merge dict: path_id -> {heading:, instructions:, path:, path_id:, scan:,}
ad_merge_dict = {}
for x in tqdm(origin_merge):
       x.pop('instructions')
       x['instructions'] = []
       ad_merge_dict[x['path_id']] = x

# ad data, used origin merge, map new instr to origin dict
new_data = [] # the list of new data, each data is a dict (path id->instr)
for fn in fns:
       with open(fn) as f:
              new_data.append(json.load(f))

for nd in new_data: # each nd is a dict, (pathid -> instr)
       for k,v in tqdm(nd.items()):
              ad_merge_dict[k]['instructions'].append(v)
ad_merge = list(ad_merge_dict.values())
json.dump(
    ad_merge,
    open('prepocess/ad_merge.json', 'w'),
    sort_keys=True, indent=4, separators=(',', ': ')
)

# split ad data
ad_sep = []
for item in ad_merge:
       for j, instr in enumerate(item['instructions']):
              new_item = dict(item)
              new_item['path_id'] = '%s_%d' % (item['path_id'], j)
              new_item['instructions'] = [instr]
              ad_sep.append(new_item)
json.dump(
    ad_sep,
    open('prepocess/ad_sep.json', 'w'),
    sort_keys=True, indent=4, separators=(',', ': ')
)

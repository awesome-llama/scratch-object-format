import converter

import json

FILES = ['code_errors.json', 'analysed_all.json', 'griffpatch.json', 'turbowarp-addon-settings.json', 'comments.json', 'cols.json', 'model1.json']


for file in FILES:
    # load
    with open(f'examples/{file}') as f:
        data = json.loads(f.read())

    output = converter.encode(data)

    with open(f'examples/converted/{file}.txt', 'w') as f:
        f.writelines([str(o)+'\n' for o in output])


    #
    
    with open(f'examples/converted/{file}.txt.json', 'w') as f:
        f.write(json.dumps(converter.decode(output), indent=2))
import os
import json


token_map = {}
root_path = os.getcwd()
for folder in os.listdir(root_path):
    token_map[folder] = {}
    log_path = os.path.join(root_path, folder, 'llm_completions')
    if not os.path.exists(log_path):
        continue
    for folder2 in os.listdir(log_path):
        folder2_path = os.path.join(root_path, folder, 'llm_completions', folder2)
        for file in os.listdir(folder2_path):
            file_path = os.path.join(root_path, folder, 'llm_completions', folder2, file)
            with open(file_path, 'r', encoding='UTF-8') as fd:
                data = json.load(fd)
                if 'token' not in token_map[folder]:
                    token_map[folder]['token'] = 0
                if 'prompt_tokens' not in token_map[folder]:
                    token_map[folder]['prompt_tokens'] = 0
                if 'completion_tokens' not in token_map[folder]:
                    token_map[folder]['completion_tokens'] = 0
                token_map[folder]['token'] += data['response']['usage']['total_tokens']
                token_map[folder]['prompt_tokens'] += data['response']['usage']['prompt_tokens']
                token_map[folder]['completion_tokens'] += data['response']['usage']['completion_tokens']

        
print(json.dumps(token_map, indent=1))



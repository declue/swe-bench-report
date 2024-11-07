import streamlit as st
import os
import json


st.set_page_config(layout="wide")

st.markdown("# SWE Bench Output Viewer")


root = os.getcwd()
folder_list = os.listdir('.')


model_info_list = []
output_map = {}

for folder in folder_list:
    model_info = {}
    output_json = []
    output_json_file = os.path.join(root, folder, 'output.jsonl') 
    metadata_json_file = os.path.join(root, folder, 'metadata.json')

    if not os.path.exists(output_json_file):
        continue
    if not os.path.exists(metadata_json_file):
        continue
    with open(os.path.join(root, folder, 'output.jsonl'), 'r', encoding='UTF-8') as fd:
      for item in list(fd):
        output_json.append(json.loads(item))
    with open(os.path.join(root, folder, 'metadata.json'), 'r', encoding='UTF-8') as fd:
      metadata_json = json.load(fd)
    logs_files = os.listdir(os.path.join(root, folder, "logs"))
    llm_completions_files = os.listdir(os.path.join(root, folder, "llm_completions"))
    model_info['metadata'] = metadata_json
    model_info['start_time'] = metadata_json['start_time']
    model_info['dataset'] = metadata_json['dataset']
    model_info['max_iterations'] = metadata_json['max_iterations']
    model_info['model'] = metadata_json['llm_config']['model']
    model_info['logs'] = logs_files
    model_info['completions'] = llm_completions_files
    output_map[model_info['model']] = output_json
    model_info_list.append(model_info)

#st.write(model_info_list[1])
model_list = {model_info['model'] : model_info for model_info in model_info_list}
selected  = st.selectbox('Model', options=list(model_list.keys()))

with st.expander("Metadata"):
    st.write(model_list[selected]['metadata'])

instance_map = {item['instance_id'] : item for item in output_map[selected]}
selected_instance = st.selectbox('instance_id', options=list(instance_map.keys()))
instance = instance_map[selected_instance]


with st.expander("Test Result"):
    st.write(instance['test_result'])

with st.expander("Instruction"):
    st.text(instance['instruction'])

completions_files = []
completion_folder = os.path.join(root, folder, 'llm_completions', selected_instance)

files = sorted(os.listdir(completion_folder))


for _file in files:
    if _file.startswith("draft"):
        continue
    file = _file
st.write(files)
st.write(file)
with open(os.path.join(completion_folder, file), 'r', encoding='UTF-8') as fd:
    json_data = json.load(fd)
    for message in json_data['messages']:
        with st.chat_message(message['role']):
            st.text(message['content'])





#for item in instance['completions']:
#
#    with st.chat_message(item['source']):
#        if 'action' in item:
#            st.markdown("### <" + str(item['id']) + ">" + item['action'])
#        st.write(item['message'])



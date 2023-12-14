from libs.process_pdf import split_pdf_pages, text_purify, get_pdf_outline
from libs.spec_prompt import *
from libs.poe import get_final_poe_response
from pprint import pprint, pformat
from collections import Counter
import ast
import asyncio
import json
import time
import math
import tiktoken

class ContextExtractor():

    def __init__(self, spec_file='docs/zcl.pdf') -> None:
        self.spec_pages = split_pdf_pages(spec_file)
        self.spec_outline = get_pdf_outline(spec_file)
        self.n_page = len(self.spec_pages)
        self.cluster_index_dict, self.cmd_index_dict, self.cmd_profile = self.summarize_inferred_cmd_info()
    
    def summarize_inferred_cmd_info(self,
                                    cmd_file='../command-re/spec/results/zcl-cmd.json',
                                    output_cluster_index_file = 'docs/cluster-index.json',
                                    output_cmd_index_file = 'docs/cmd-index.json'):
       cmd_json_dict = {}
       # Dict which only contains cluster name, command name, field name, field data type
       cluster_dict = {}
       cmd_dict = {}
       summary_dict = {}
       with open(cmd_file, 'r') as fp:
           cmd_json_dict = json.load(fp)
           for cid, cluster_info in cmd_json_dict.items():
               cid_val = int(cid, 16)
               cluster_name = cluster_info['name']
               cluster_dict[cid_val] = cluster_name
               cmd_dict[cid_val] = {}
               summary_dict[cluster_name] = {} 
               for cmd_id, cmd_info in cluster_info['cmds'].items():
                   cmd_id_val = int(cmd_id, 16)
                   cmd_name = cmd_info['description']
                   cmd_dict[cid_val][cmd_id_val] = cmd_name
                   cmd_payloads = cmd_info['payload']
                   summary_dict[cluster_info['name']][cmd_name] = {}
                   for field_name, field_info in cmd_payloads.items():
                       if field_name == '...':
                           break
                       summary_dict[cluster_info['name']][cmd_name][field_name] = field_info['type']

       with open(output_cluster_index_file, 'w') as fp:
           fp.write(json.dumps(cluster_dict))
       with open(output_cmd_index_file, 'w') as fp:
           fp.write(json.dumps(cmd_dict))
       return cluster_dict, cmd_dict, summary_dict

    def extract_cmd_descriptions(self, output_file='docs/cmd-description.json'):
        answer_dict = {}
        for cluster_name, cluster_cmds in self.cmd_profile.items():
            cid = [k for k in self.cluster_index_dict.keys() if self.cluster_index_dict[k] == cluster_name][0]
            answer_dict[cid] = {}
            for cmd_name, cmd_fields in cluster_cmds.items():
                cmd_id = [k for k in self.cmd_index_dict[cid].keys() if self.cmd_index_dict[cid][k] == cmd_name][0]
                answer_dict[cid][cmd_id] = ''
                # Build the purified command name for searching
                purified_cmd_name = ''
                if cmd_name in ['DiscoverCommandsReceivedResponse', 'DiscoverCommandsGeneratedResponse', 'Execution of a Command', 'GetWeeklySchedule', 'GetRelayStatusLog', 'GetWeeklySchedule', 'GetRelayStatusLog', 'GoToLiftValue', 'GotoLiftPercentage', 'GotoTiltValue', 'GotoTiltPercentage']:
                    purified_cmd_name = text_purify(cmd_name)
                else:
                    purified_cmd_name = text_purify(cmd_name.split('(')[0]+'command') # For some command names with (With On/Off) additional name subfix, we don't care the subfix
                # Identify suitable section entries based on the section name
                candidate_outline_entries = []
                for x in self.spec_outline:
                    section_title_seg = x[1].split(' ', 1)
                    if len(section_title_seg) >= 2 and text_purify(section_title_seg[1]) == purified_cmd_name:
                        candidate_outline_entries.append(x)
                #candidate_outline_entries = [x for x in self.spec_outline if purified_cmd_name == text_purify(x[1].split(' ', 1)[1])]
                #if len(candidate_outline_entries) == 0:
                #    purified_cmd_name = text_purify(cmd_name)
                #    candidate_outline_entries = [x for x in self.spec_outline if purified_cmd_name == text_purify(x[1].split(' ', 1)[1])]
                if len(candidate_outline_entries) > 0:
                    selected_entry = min(candidate_outline_entries, key=lambda p:p[0]); entry_index = self.spec_outline.index(selected_entry)
                    entry_level = selected_entry[0]
                    start_page = selected_entry[2] - 1
                    closest_entry_with_same_level = [x for x in self.spec_outline[entry_index+1:] if x[0] <= entry_level][0]
                    end_page = closest_entry_with_same_level[2] - 1
                    answer_dict[cid][cmd_id] = ''.join(self.spec_pages[start_page:end_page+1])
                    #print(f"For command ({cluster_name}:{cmd_name}):\n Start page, end page = ({start_page, end_page})")
                else:
                    print(f"Missing outline entries for command ({cluster_name}:{cmd_name})")
        with open(output_file, 'w') as fp:
            fp.write(json.dumps(answer_dict))

class CmdAnalyzer():
    
    def __init__(self, cluster_index_file = 'docs/cluster-index.json',
                 cmd_index_file = 'docs/cmd-index.json',
                 cmd_description_file='docs/cmd-description.json',
                 summarized_cmd_description_file='docs/cmd-summarized-description.json'):
        
        self.async_loop = asyncio.get_event_loop()
        self.cluster_dict = {}
        self.cmd_dict = {}
        self.cmd_description_dict = {}
        self.summarized_cmd_description_dict = {}
        with open(cluster_index_file, 'r') as fp:
            self.cluster_dict = json.load(fp)
        with open(cmd_index_file, 'r') as fp:
            self.cmd_dict = json.load(fp)
        with open(cmd_description_file, 'r') as fp:
            self.cmd_description_dict = json.load(fp)
        with open(summarized_cmd_description_file, 'r') as fp:
            self.summarized_cmd_description_dict = json.load(fp)
        if len(self.summarized_cmd_description_dict.keys()) == 0:
            self.summarize_description()

    def num_tokens_from_messages(self, messages, model="gpt-3.5-turbo-0613"):
      """Returns the number of tokens used by a list of messages."""
      try:
          encoding = tiktoken.encoding_for_model(model)
      except KeyError:
          encoding = tiktoken.get_encoding("cl100k_base")
      if model == "gpt-3.5-turbo-0613":  # note: future models may deviate from this
          num_tokens = 0
          for message in messages:
              num_tokens += 4  # every message follows <im_start>{role/name}\n{content}<im_end>\n
              for key, value in message.items():
                  num_tokens += len(encoding.encode(value))
                  if key == "name":  # if there's a name, the role is omitted
                      num_tokens += -1  # role is always required and always 1 token
          num_tokens += 2  # every reply is primed with <im_start>assistant
          return num_tokens
      else:
          raise NotImplementedError(f"""num_tokens_from_messages() is not presently implemented for model {model}.
      See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens.""")
        
    def get_tokens(self, contents:'list[str]'):
        num_tokens = []
        for content in contents:
            num_token = self.num_tokens_from_messages([{"role": "user", "content":content}])
            num_tokens.append(num_token)
        print(Counter(num_tokens))
        print(f"Max token: {max(num_tokens)}")
        return num_tokens
    
    async def async_summarize_description(self):
        cmd_infos = [(x,y,self.cmd_description_dict[x][y]) for x in self.cmd_description_dict.keys() for y in self.cmd_description_dict[x].keys()]
        cmd_name_description_pairs = [(self.cmd_dict[cmd_info[0]][cmd_info[1]],cmd_info[2]) for cmd_info in cmd_infos]
        prompts = []
        for cmd_name_description_pair in cmd_name_description_pairs:
            prompt = DESCRIPTION_SUMMARY_PROMPT.format(cmd_name_description_pair[0], cmd_name_description_pair[1])
            prompts.append(prompt)
            
        num_tokens = self.get_tokens(prompts)
        llm_answers = []
        query_each_round = 100
        n_round = len(prompts) / query_each_round
        print(f"Total round = {n_round}")
        start_time = time.time()
        for i in range(math.ceil(n_round)):
            tasks = [get_final_poe_response(prompt, .5) for prompt in prompts[i*query_each_round:(i+1)*query_each_round]]
            llm_part_answers =  await asyncio.gather(*tasks)
            llm_answers = llm_answers + llm_part_answers
            print(f"Round {i} ... finished!")
            print(f"Consumed time: {(time.time()-start_time)*1./60} minutes")
        
        ## Some command descriptions are still too long... Followings for error debuging
        #empty_answer_indices = [x for x in range(len(llm_answers)) if llm_answers[x] == '']
        #print([num_tokens[i] for i in empty_answer_indices])
        #refined_num_tokens = self.get_tokens(llm_answers)
        
        for i, cmd_info in enumerate(cmd_infos):
            cid = cmd_info[0]; cmd_id = cmd_info[1]; cmd_refined_description = llm_answers[i]
            self.summarized_cmd_description_dict[cid] = {} if cid not in self.summarized_cmd_description_dict.keys() else self.summarized_cmd_description_dict[cid]
            self.summarized_cmd_description_dict[cid][cmd_id] = cmd_refined_description
        with open('docs/cmd-summarized-description.json', 'w') as fp:
            fp.write(json.dumps(self.summarized_cmd_description_dict))
    
    async def cmd_dependency_construction(self, case_id=0):
        start_time = time.time()
        cmd_info = [(x,y,self.summarized_cmd_description_dict[x][y]) for x in self.summarized_cmd_description_dict.keys() for y in self.summarized_cmd_description_dict[x].keys()]
        cmd_pairs = [(x, y) for x in cmd_info for y in cmd_info]
        prompts = []
        num_tokens = []
        for cmd_pair in cmd_pairs:
            preceding_cmd_name = self.cmd_dict[cmd_pair[0][0]][cmd_pair[0][1]]
            consecutive_cmd_name = self.cmd_dict[cmd_pair[1][0]][cmd_pair[1][1]]
            preceding_cmd_desc = cmd_pair[0][2]
            consecutive_cmd_desc = cmd_pair[1][2]
            prompt = CMD_DEPENDENCY_PROMPT.format(preceding_cmd_name, preceding_cmd_desc,
                                                   consecutive_cmd_name, consecutive_cmd_desc)
            prompts.append(prompt)
        llm_answers = []
        query_each_round = 100
        n_round = len(prompts) / query_each_round
        print(f"Total round = {n_round}")
        for i in range(math.ceil(n_round)):
            tasks = [get_final_poe_response(prompt, .5) for prompt in prompts[i*query_each_round:(i+1)*query_each_round]]
            llm_part_answers =  await asyncio.gather(*tasks)
            llm_answers = llm_answers + llm_part_answers
            print(f"Round {i} ... finished!")
            print(f"        Consumed time for round {i}: {(time.time()-start_time)*1./60} minutes")
        end_time = time.time()
        print(f"Total consumed time: {(end_time-start_time)*1./60} minutes")
        with open(f'inter_result/dependency-reason-case{case_id}.txt', 'w') as fp:
            fp.write('\n\n'.join(llm_answers))
        
        dependency_result = [((cmd_pairs[i][0][0], cmd_pairs[i][0][1]), (cmd_pairs[i][1][0], cmd_pairs[i][1][1]), text_purify(DEPENDENCY_KEYWORD) in text_purify(answer)) for i, answer in enumerate(llm_answers)]
        return dependency_result
    
    def construct_msg_dependency(self, n_trails=1, output_file='analysis_result/msg-dependency.txt'):
        all_dependency_results = []
        for i in range(n_trails):
            dependency_result = self.async_loop.run_until_complete(self.cmd_dependency_construction(i))
            all_dependency_results = all_dependency_results + dependency_result
        result_frequencies = dict(Counter(all_dependency_results))
        frequent_results = [k for k, v in result_frequencies.items() if v>n_trails/2]
        dependency_relationship = []
        for final_result in frequent_results:
            if final_result[-1] is True:
                # A command dependency relationship is identified!
                preceding_cmd_info = final_result[0]
                consecutive_cmd_info = final_result[1]
                dependency_relationship.append([preceding_cmd_info, consecutive_cmd_info])
        with open(output_file, 'w') as fp:
            fp.write(str(dependency_relationship))
        
        ## Test parsing the written result in the file
        #with open(output_file, 'r') as fp:
        #    content = fp.readline().strip()
        #    dependency_list = ast.literal_eval(content)
        #    print(dependency_list)
    
    def summarize_description(self):
        task = self.async_loop.create_task(self.async_summarize_description())
        self.async_loop.run_until_complete(task)
        return task.result()

if __name__ == '__main__':
    #context_extractor = ContextExtractor()
    #context_extractor.extract_cmd_descriptions()
    
    cmd_analyzer = CmdAnalyzer()
    #cmd_analyzer.summarize_description()
    cmd_analyzer.construct_msg_dependency(n_trails=5)
    
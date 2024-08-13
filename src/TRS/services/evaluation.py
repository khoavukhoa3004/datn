import json, os
from constants import PATH_EVAL_FOLDER

def validate_dic_of_evaluation(dic):
    assert('cur_user_level' in dic)
    assert('pre_question_idx' in dic)
    assert('list_eval_question' in dic)
    assert('total_eval_questions' in dic)
    assert('list_eval_level' in dic)

def writeEvalFile(user_id, cur_level, dic):
    validate_dic_of_evaluation(dic)
    
    file_name = f'{user_id}_{cur_level}.json'
    file_dir = os.path.join(PATH_EVAL_FOLDER, file_name)
    with open(file_dir, 'w') as outfile:
        outfile.write(json.dumps(dic, indent=2))
        
def updateEvalFile_AppendEvalQuestion(user_id, cur_level, new_ques_id, new_ques_level):
    res = readEvalFile(user_id, cur_level)
    assert(res[0] == -1 and res[0] != -2)
    _, eval_dic = res
    eval_dic['list_eval_question'].append({'id': new_ques_id, 'level': new_ques_level})
    eval_dic['total_eval_questions'] += 1
    writeEvalFile(user_id, cur_level, eval_dic)

def readEvalFile(user_id, cur_level, dic_out):
    '''
    -   if file not exist:
            return -2
    -   if 'pre_question_idx' < ':
            increase idx
            :return: next level to suggest
    -   else:
            return -1
            
    - if has file and remains level to suggest:
        return True
    - else: 
        return False
    '''
    file_name = f'{user_id}_{cur_level}.json'
    file_dir = os.path.join(PATH_EVAL_FOLDER, file_name)
    
    if not os.path.exists(file_dir):
        return False
    
    with open(file_dir, 'w+') as eval_json:
        eval_dic = json.load(eval_json)
        validate_dic_of_evaluation(eval_dic)
        
        if eval_dic['pre_question_idx'] >= eval_dic['total_eval_questions'] - 1:
            return False
        
        else:
            dic_out['eval_level'] = eval_dic['list_eval_level'][eval_dic['pre_question_idx']]
            dic_out['eval_dic'] = eval_dic
            return True

def createEvaluationDictionary(n_eval_questions, cur_user_level, first_ques_id, first_ques_level, list_eval_level):
    dic = {
        'cur_user_level': cur_user_level,
        'pre_question_idx': 0,
        'total_eval_questions': 2 * n_eval_questions,
        'list_eval_level': list_eval_level,
        'list_eval_question': [
            {
                'id': first_ques_id,
                'level': first_ques_level,
            }
        ]
    }
    
    return dic


import csv, torch
import pandas as pd
from llama_cpp import Llama

# GLOBAL VARIABLES
# llama_model = Llama(model_path="/data/prathish/Llama_train/llama.cpp/models/models--TheBloke--Llama-2-7b-Chat-GGUF/snapshots/191239b3e26b2882fb562ffccdd1cf0f65402adb/llama-2-7b-chat.Q5_K_S.gguf")#, **model_kwargs)
my_model_path = "/data/shared/huggingface/hub/models--TheBloke--Llama-2-7b-Chat-GGUF/snapshots/191239b3e26b2882fb562ffccdd1cf0f65402adb/llama-2-7b-chat.Q5_K_S.gguf"

# LOAD THE MODEL
llama_model = Llama(model_path=my_model_path)


def convert_to_norm(mixtral_model_response):
    prefix2norm = {
        'Yes': 1,
        'No': 0
    }
    
    invalid = -1
    
    final_result = mixtral_model_response["choices"][0]["text"].strip()
    first_word = final_result.split()[0]
    value = first_word.rstrip('.!?,')

    for prefix, norm in prefix2norm.items():
        if prefix.lower() == value.lower():
            return norm
    return invalid



def generate_text_from_prompt(user_prompt,
                              max_tokens=500,
                              temperature=0.3,
                              top_p=0.1,
                              echo=True):
    
    prompt = f"[INST] {user_prompt} [/INST]"
    
    # Define the parameters
    with torch.no_grad():
        model_output = Llama(
            prompt,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            echo=echo
        )
    return model_output



def main(outputFileName, inputFileName):
    
    df = pd.read_csv(inputFileName).head(500)

    with open(outputFileName, 'w', newline='') as csvoutput:
        writer = csv.writer(csvoutput, lineterminator='\n')
        writer.writerow(['question_id', 'rung', 'prompt', 'truth', 'truth_norm', 'pred', 'pred_norm', 'model_version'])

        for i in range(df.shape[0]):
            prompt = df.at[i, 'prompt']
            question_id = df.at[i, 'question_id']
            truth = df.at[i, 'truth']
            rung = df.at[i, 'rung']
            truth_norm = df.at[i, 'truth_norm']
            mixtral_model_response = generate_text_from_prompt(prompt)
            
            final_result = mixtral_model_response["choices"][0]["text"].strip()

            pred_norm = convert_to_norm(mixtral_model_response)

            writer.writerow([question_id, rung, prompt, truth, truth_norm, final_result, pred_norm, 'mixtral_8x7b_instruct_gguf'])
            
            
if __name__ == '__main__':
    outputFileName = "/data/shared/Mixtral_train/Cladder/test_mixtral_gguf_causal_benchmark_results.csv"
    inputFileName = "/data/prathish/Llama_train/Cladder/test_causal_benchmark_data_llama_2.csv"
    main(outputFileName, inputFileName)
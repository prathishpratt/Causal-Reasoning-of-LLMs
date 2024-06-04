import csv, torch
import pandas as pd
from llama_cpp import Llama

# GLOBAL VARIABLES
# llama_model = Llama(model_path="/data/prathish/Llama_train/llama.cpp/models/models--TheBloke--Llama-2-7b-Chat-GGUF/snapshots/191239b3e26b2882fb562ffccdd1cf0f65402adb/llama-2-7b-chat.Q5_K_S.gguf")#, **model_kwargs)
my_model_path = "/data/shared/huggingface/hub/models--TheBloke--Llama-2-7b-Chat-GGUF/snapshots/191239b3e26b2882fb562ffccdd1cf0f65402adb/llama-2-7b-chat.Q5_K_S.gguf"

# LOAD THE MODEL
llama_model = Llama(model_path=my_model_path)


def convert_to_norm(llama_model_response):
    prefix2norm = {
        'Yes': 1,
        'No': 0
    }
    
    invalid = -1
    
    final_result = llama_model_response["choices"][0]["text"].strip()
    parts = final_result.split("[/INST]")
    following_text = parts[1].strip()  # Remove any leading whitespace
    first_word = following_text.split()[0]
    value = first_word.rstrip('.!?,')

    for prefix, norm in prefix2norm.items():
        if prefix.lower() == value.lower():
            return norm
    return invalid


def generate_text_from_prompt(user_prompt,
                             max_tokens = 500,
                             temperature = 0.3,
                             top_p = 0.1,
                             echo = True):
    
    prompt = f"""[INST] <<SYS>>
    You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe.  Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature. If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information.
    <</SYS>>
    {user_prompt}[/INST]"""
    
    
    # Define the parameters
    with torch.no_grad():
   # Define the parameters
        model_output = llama_model(
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
            llama_model_response = generate_text_from_prompt(prompt)
            
            final_result = llama_model_response["choices"][0]["text"].strip()
            prompt_end_marker = "[/INST]  "  # The prompt ends with this marker followed by two spaces
            start_index = final_result.find(prompt_end_marker) + len(prompt_end_marker)

            # Extract the model-generated text after the prompt
            outputs = final_result[start_index:].strip()
            
            pred_norm = convert_to_norm(llama_model_response)

            writer.writerow([question_id, rung, prompt, truth, truth_norm, outputs, pred_norm, 'llama2_gguf'])
            
            
if __name__ == '__main__':
    outputFileName = "/data/prathish/Llama_train/Cladder/test_llama_gguf_causal_benchmark_results.csv"
    inputFileName = "/data/prathish/Llama_train/Cladder/test_causal_benchmark_data_llama_2.csv"
    main(outputFileName, inputFileName)
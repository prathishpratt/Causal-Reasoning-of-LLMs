import csv, torch
import pandas as pd
from llama_cpp import Llama

# GLOBAL VARIABLES
# llama_model = Llama(model_path="/data/prathish/Llama_train/llama.cpp/models/models--TheBloke--claude2-alpaca-7B-GGUF/snapshots/73099953ac68a3b9d3d8004bd5f2debc2986cd5b/claude2-alpaca-7b.Q2_K.gguf")#, **model_kwargs)
my_model_path = "/data/shared/huggingface/hub/models--TheBloke--claude2-alpaca-7B-GGUF/snapshots/73099953ac68a3b9d3d8004bd5f2debc2986cd5b/claude2-alpaca-7b.Q2_K.gguf"

# LOAD THE MODEL
llama_model = Llama(model_path=my_model_path)


def convert_response_to_numeric(text_input):
    prefix2norm = {
        'Yes': 1,
        'No': 0
    }
    
    invalid = -1
    sections = text_input.split('\n\n### ')
    if len(sections) < 2:
        return invalid
    
    response_with_excess = sections[1].split('\n\n')[0]
    response = response_with_excess.strip()
    
    return prefix2norm.get(response, invalid)


def generate_text_from_prompt(user_prompt,
                             max_tokens = 500,
                             temperature = 0.3,
                             top_p = 0.1,
                             echo = True):
    
    prompt = f"""Below is an instruction that describes a task. Write a response that appropriately completes the request.

    {user_prompt}
    """
    
    
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
    df = pd.read_csv(inputFileName).head(2)

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
            pred_norm = convert_response_to_numeric(final_result)

            writer.writerow([question_id, rung, prompt, truth, truth_norm, final_result, pred_norm, 'alpaca_gguf'])

            
            
if __name__ == '__main__':
    outputFileName = "/data/prathish/Llama_train/Cladder/test_alpaca_gguf_causal_benchmark_results.csv"
    inputFileName = "/data/prathish/Llama_train/Cladder/test_causal_benchmark_data_llama_2.csv"
    main(outputFileName, inputFileName)
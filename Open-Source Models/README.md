## Open Source Models

### Models we used:
 
- Llama 2 🦙, Alpaca 🦙 and Mixtral-8x7B 

### Problems with Open-Source Models:

- Significant computational resources like GPU/TPU
- To run the 7B model in full precision, you need 7 * 4 = 28GB of GPU RAM !!
- Locally stored ⇒ Means higher disk space needed
- The size of llama-2-13B is ≈ 25GB !!
- Lots of dependencies 

## Solution: Quantization

Quantization is a technique used to reduce the size and memory usage while maintaining quality 
of the LLM.  Done by reducing the precision of the model parameters and weights. 

We chose to use quantized versions of the models, such as the [Llama-2-7B-Chat-GGUF](https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF) and [Mixtral-8x7B-Instruct-v0.1-GGUF](https://huggingface.co/TheBloke/Mixtral-8x7B-Instruct-v0.1-GGUF)


The reduction is achieved by GGUF quantization method through **llama.cpp**, allowing them to run efficiently on CPUs **without the need for GPU support**.

| Model      | Size Before Quantization | Size After Quantization |
|------------|--------------------------|-------------------------|
| Llama2 7B  | ≈ 15 GB                  | ≈ 6 GB                  |
| Alpaca 7B  | ≈ 15 GB                  | ≈ 6 GB                  |
| Mixtral 8x7B (Ollama) | ≈ 26 GB       | ≈ 15 GB                 |

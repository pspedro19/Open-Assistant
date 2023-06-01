from flask import Flask, jsonify, request
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import os

app = Flask(__name__)

os.environ["CUDA_VISIBLE_DEVICES"] = "0"

MODEL_NAME = "oasst-sft-4-pythia-12b-epoch-3.5"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)
model=model.half().cuda()

if torch.cuda.is_available():
    model = model.to('cuda')
    model = model.half()

@app.route('/', methods=['POST'])
def generate():
    text = request.json['text']
    inputs = tokenizer.encode(text + tokenizer.eos_token, return_tensors='pt')
    
    if torch.cuda.is_available():
        inputs = inputs.to('cuda')
    
    outputs = model.generate(inputs, max_length=1000, pad_token_id=tokenizer.eos_token_id)
    decoded_output = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return jsonify({"generated_text": decoded_output})

if __name__ == '__main__':
    app.run(port=5000)

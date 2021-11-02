#!/usr/bin/python3
# -*- coding: utf-8 -*-

from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# https://huggingface.co/liam168/chat-DialoGPT-small-zh
_model_dir = '/Users/liampro/Downloads/dataLake/Models/nlp/huggingface/liam168/chat-DialoGPT-small-zh'

class NLPChat:
    def __init__(self,model_dir=_model_dir):
        self.tokenizer = AutoTokenizer.from_pretrained(model_dir)
        self.model = AutoModelForCausalLM.from_pretrained(model_dir)

    def dialog(self,ask ,history_ids =[] ):
        inputs = ask + self.tokenizer.eos_token
        print('-'*100)
        print('Question:',inputs)
        new_user_input_ids = self.tokenizer.encode( inputs, return_tensors='pt')
        #print('new_user_input_ids:',new_user_input_ids)

        bot_input_ids = new_user_input_ids
        #bot_input_ids = torch.cat([history_ids, new_user_input_ids], dim=-1) if len(history_ids) > 0 else new_user_input_ids
        #print('bot_input_ids:',bot_input_ids)
        chat_history_ids = self.model.generate(bot_input_ids, max_length=100, pad_token_id=self.tokenizer.eos_token_id)
        #print('chat_history_ids:',chat_history_ids)

        #print("1 DialoGPT: {}".format(tokenizer.decode(chat_history_ids[0], skip_special_tokens=True)))
        answer = self.tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
        print("Answer: {}".format(self.tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)))
        return chat_history_ids, ask,answer
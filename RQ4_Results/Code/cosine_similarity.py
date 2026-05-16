import json
import os
import torch
import pandas as pd
import matplotlib.pyplot as plt
from transformers import BertTokenizer, BertModel
from sklearn.metrics.pairwise import cosine_similarity



# Load the BERT model and tokenizer
device    = torch.device("cuda" if torch.cuda.is_available() else "cpu") 
BERT_tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
BERT_model     = BertModel.from_pretrained("bert-base-uncased").to(device)
BERT_model.eval()



main_dir = "" # set your working directory
output_dir = os.path.join(main_dir, "cosine_scores.csv")
plot_png = os.path.join(main_dir, "cosine_score_dist.png")
conf_list = ["ESEM", "EASE", "SANER"]



# Converts title and abstract to vector using BERT
def convert_to_vector(title_and_abstract):
    tokenized_text = BERT_tokenizer(title_and_abstract, return_tensors="pt", truncation=True, padding=True).to(device)
    with torch.no_grad():
        bert_output = BERT_model(**tokenized_text)
    
    return bert_output.last_hidden_state[:, 0, :].cpu().numpy() #


# concatenates the title and abstract
def concat_title_abstract(paper_json):
    title = paper_json.get("title", "")
    abstract = paper_json.get("abstract", "")
    return f"{title} {abstract}"







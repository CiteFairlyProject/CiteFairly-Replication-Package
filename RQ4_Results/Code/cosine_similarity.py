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



main_dir = "" # set your working directory that contains the json files for ESEM, EASE, and SANER
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


cosine_scores = []


for conf in conf_list:
    conf_dir = os.path.join(main_dir, conf) # direcotry for each conferences in working directory
    json_files = os.listdir(conf_dir)

    for json_file in json_files:
        with open(os.path.join(conf_dir, json_file), "r") as f:
            paper_json = json.load(f) #loads the json file for each paper in the conference
        
        paper_vector = convert_to_vector(concat_title_abstract(paper_json)) # converts the title and abstract to vector using BERT

        recommendation = paper_json.get("related", []) 

        for rec in recommendation:
            recommendation_vector = convert_to_vector(concat_title_abstract(rec)) # converts title and abstract of each recommended paper to vector

            cosine_score = cosine_similarity(paper_vector, recommendation_vector)[0][0] # calculates the cosine score

            cosine_scores.append({
                "conference":   conf,
                "year":         paper_json.get("year", ""),
                "paper":        paper_json.get("title", ""),
                "rec_title":    rec.get("title", ""),
                "cosine_score": float(cosine_score),
            })


# converts the cosine scores to DataFrame for a plot and save it as CSV
df = pd.DataFrame(cosine_scores)
df.to_csv(output_dir, index=False)


# plots the dictriubution of cosine scores for ESEM, EASE, and SANER
fig, ax = plt.subplots(figsize=(8, 5))

group_by_conf =[]

# groups the cosine scores by conference for the plot 
for conf in conf_list:
    c_scores =df[df["conference"] == conf]["cosine_score"].values
    group_by_conf.append(c_scores)

colors = ["#1f78b5", "#059635", "#fc6f28"]

box_plot= ax.boxplot(group_by_conf, labels=conf_list,patch_artist=True, medianprops=dict(color="black", linewidth=2.5) ) 

legend = []

# the loop assigns colors, transparency, and legend
for box, color, conf in zip(box_plot["boxes"], colors, conf_list): 
    box.set_facecolor(color) #sets colors for conferces
    box.set_alpha(0.7) # add transparency 
    legend.append(plt.Rectangle((0, 0), 1, 1, fc=color, alpha=0.7, label=conf)) #add legend

legend.append(plt.Line2D([0], [0], color="black", linewidth=2.5, label="Median")) # median line for box plot


ax.set_xlabel("Conference", fontsize=11)
ax.set_ylabel("Cosine Similarity Score", fontsize=11)
ax.set_title("Cosine Similarity Score Distribution of ESEM, EASE, and SANER", fontsize=12)
ax.set_ylim(0, 1)
ax.legend(handles=legend, loc="lower right")
ax.grid(axis="y", linestyle="--", alpha=0.5)

plt.tight_layout()
plt.savefig(plot_png, dpi=300)
plt.show()







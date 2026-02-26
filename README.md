# CiteFairly-Replication-Package
Replication package for the CiteFairly study


## RQ3: Accuracy of CiteFairly Compared to Manual Gender Annotation

RQ3 evaluates whether CiteFairly can generate an overall author gender distribution that closely matches a manually verified distribution. This is important because Citation Diversity Statements (CDSs) are only meaningful if the underlying gender inference is reliable.

### Overall Findings

CiteFairly’s automated gender assignments were highly consistent with manual human annotations. Across all three software engineering conferences (ESEM, EASE, SANER), the average absolute difference between CiteFairly and manual labels remained within 5 percentage points.

As stated in the paper:  
> “The average absolute difference between manual and automated CiteFairly results was approximately 1.4% across all eleven papers…”  
> 

### Data Used for RQ3

To evaluate CiteFairly, the authors manually analyzed a subset of the full dataset:

- A 5% sample of all reference lists was selected (55 papers out of 1,075).  
- These 55 papers contained 1,150 cited references.  
- Across those references, 3,783 individual authors were manually gender‑annotated.  
- Manual gender identification used publicly available sources such as institutional profiles, personal websites, and LinkedIn.

### How CiteFairly Was Evaluated

1. Manual gender labels were created for all authors in the sampled reference lists.  
2. CiteFairly automatically assigned gender labels using Gender‑API.  
3. For each paper, the distribution of male, female, and unknown authors was computed manually and automatically.  
4. The absolute difference between the two distributions was calculated.  
5. Results were aggregated by conference (ESEM, EASE, SANER).

### How to Replicate the RQ3 Evaluation

Anyone can reproduce the RQ3 results by following these steps:
Note: the exact data set used is given here under RQ3_Results --> Data

1. **Collect a reference list dataset**  
   - Export reference lists from a set of SE conference papers (e.g., ESEM, EASE, SANER).  
   - Use BibTeX or plain text files.

2. **Manually annotate author genders**  
   - For each cited paper, list all authors.  
   - Identify gender using publicly available sources (institutional pages, LinkedIn, personal websites).  
   - Record gender as:  
     - `male`  
     - `female`  
     - `unknown` (if gender cannot be confidently determined)

3. **Run CiteFairly on the same reference lists**  
   - Upload the reference list to CiteFairly.  
   - Allow CiteFairly to infer gender using Gender‑API.  
   - Export the automated gender distribution.

4. **Compute distribution differences**  
   - For each reference list, compute the percentage of male, female, and unknown authors manually.  
   - Compute the same percentages using CiteFairly.  
   - Calculate the absolute difference for each category.  
   - Average the differences across all sampled papers.

5. **Compare results**  
   - Differences within 5 percentage points indicate high agreement.  
   - Larger differences typically occur for ambiguous, initial‑only, or non‑Western names.

### Interpretation

The RQ3 evaluation demonstrates that CiteFairly reliably approximates human‑verified gender distributions. Minor discrepancies are expected due to ambiguous or culturally diverse names, but overall accuracy is sufficient for generating meaningful Citation Diversity Statements.


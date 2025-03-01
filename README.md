# **ecoliframalpha**  
*A Simulation Tool for Protein Synthesis Stability in* E. coli  

---

## 📌 **Project Overview**  
**ecoliframalpha** is a Python-based simulation tool designed to model how *E. coli* manages protein synthesis stability under varying nutrient conditions. This project explores computational approaches such as **Monte Carlo simulations, Hill functions, and Markov Chains** to simulate the synthesis rate of robust and sensitive codons.  

This simulation serves as an alternative to **wet-lab experiments**, demonstrating how computational models can provide insights into biological processes. The project also incorporates **Generalized Linear Models (GLMs) and Bayesian hierarchical models** to quantify synthesis rate stability across codon categories. This project was created by David Oleksy and later further developed by Rubén Crespo Blanco.

---

## 🎥 **Demonstration Video**  
📺 Watch the project overview on YouTube:  
🔗 [**https://youtu.be/om0iujvwx9M**](https://youtu.be/om0iujvwx9M)

---

## 📖 **Scientific Motivation & Proposal**  
The primary goal of this project is to develop a **stochastic simulation** that models how *E. coli* adapts protein synthesis under **stress conditions**, particularly changing nutrient levels.  

### **Key Computational Techniques:**
- ✅ **Monte Carlo Simulations** – To model stochastic variations in synthesis rates.  
- ✅ **Hill Functions** – To describe enzyme kinetics in response to nutrient availability.  
- ✅ **Markov Chains** – To simulate codon state transitions over time.  
- ✅ **GLMs & Bayesian Hierarchical Models** – For data analysis and quantification of synthesis rate stability.  

This tool will provide a **computational framework** to study codon degeneracy lifting mechanisms and their impact on translation efficiency. The findings will be compiled into a structured scientific report following the **standard experimental format**.

---

## 🚀 **Installation Guide**  
### **🔹 Prerequisites**
Ensure you have **Python 3.7+** installed. You can check your version with:  
```bash
python --version
```

It is recommended to install the package in a virtual environment to avoid conflicts:
```bash
# Create a virtual environment (optional but recommended)
python -m venv ecoli_env
source ecoli_env/bin/activate  # On macOS/Linux
ecoli_env\Scripts\activate     # On Windows
```

###🔹 Installing the Package

To install ECOLI-FRAM ALPHA, clone this repository and install dependencies:
```bash
git clone https://github.com/yourusername/ecoliframalpha.git
cd ecoliframalpha
pip install -e .
```
Or:
```bash
pip install https://github.com/Doleks995/ecoliframalpha
```

Alternatively, if using requirements.txt:
```bash
pip install -r requirements.txt
```

##⚙️ Usage Examples
###1️⃣ Running the Simulation

Once installed, you can run the simulation using:
```bash
python -m ecoliframalpha
```
Or:
```bash
ecoliframalpha
```

###2️⃣ Using the package for Custom Simulations

You can also use the package as a Python module:
```bash
from ecoliframalpha.nutrient_stress import apply_nutrient_stress
```

## 📝 Scientific References

The following research papers and resources were consulted in the development of this simulation tool:

### **Primary References**  
- [Quantifying shifts in natural selection on codon usage between protein regions: a population genetics approach](https://bmcgenomics.biomedcentral.com/articles/10.1186/s12864-022-08635-0)  
- [Global and gene-specific translational regulation in Escherichia coli across different conditions](https://journals.plos.org/ploscompbiol/article?id=10.1371%2Fjournal.pcbi.1010641)  
- [Oxidative stress strongly restricts the effect of codon choice on the efficiency of protein synthesis in Escherichia coli](https://www.frontiersin.org/journals/microbiology/articles/10.3389/fmicb.2022.1042675/full)  

### **Additional References**  
- [The Influence of the Nucleotide Composition of Genes and Gene Regulatory Elements on the Efficiency of Protein Expression in Escherichia coli](https://link.springer.com/article/10.1134/S0006297923140109)  
- [Coping with stress: How bacteria fine-tune protein synthesis and protein transport](https://www.jbc.org/article/S0021-9258%2823%2902191-9/fulltext)  
- [An exploratory in silico comparison of open-source codon harmonization tools](https://microbialcellfactories.biomedcentral.com/articles/10.1186/s12934-023-02230-y)  
- [Environmental perturbations lift the degeneracy of the genetic code to regulate protein levels in bacteria](https://arxiv.org/abs/1212.1537?utm)  
- [Defining the Precision and Sequence Determinants of Protein Synthesis Rates](https://dspace.mit.edu/handle/1721.1/147460)  
- [LibreTexts - Steps of Translation](https://bio.libretexts.org/Courses/Lumen_Learning/Biology_for_Non_Majors_I_%28Lumen%29/10%3A_DNA_Transcription_and_Translation/10.08%3A_Steps_of_Translation)  

---

## 🎯 Potential future Work & Improvements  

- 🛠 **Optimizing Performance** – Implementing further improvements in the model 
- 📊 **Advanced Visualization** – Adding more detailed plots for analysis.  
- 🧬 **Extending to Other Organisms** – Generalizing the model beyond *E. coli*.  

---

## 💡 Contributing  

Contributions are welcome!

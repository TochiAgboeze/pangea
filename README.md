# PANGEA - Predictive Analytics and Genotypic Evaluation for AMR in Africa
This README file provides information about the packages and datasets used in the code provided.

# Problem Statement
Antimicrobial resistance (AMR) surveillance in Africa primarily use traditional antimicrobial susceptibility testing (AST) methods, which are ineffective for early detection of pathogenic outbreaks and frequently fail to discover resistance mechanisms. Although next-generation sequencing (NGS) offers a more comprehensive understanding of these systems, its high cost and resource limitations prevent widespread adoption throughout the continent.


To address these challenges, we utilised existing AST data to predict resistance gene profiles, providing a cost-effective and accessible means to gain genotypic insights. This approach enhanced the speed and accuracy of outbreak detection and bolster public health interventions in Africa, where genomic surveillance resources are limited. Our web application (PANGEA) is a web application that provides:
## Explorative Data Analysis
Insightful visualisations that provide detailed explorative data summaries of the ATLAS dataset, with visualisations ranging from AMR determinant genes theme-focused to global-scale data summaries.
## Comparative Analysis
In-depth comparative analyses conducted to identify predictors of poor AMR stewardship in Africa and pain points in the existing data for the surveillance work in Africa. This details a comparative markdown detailing statistical inference of data comparism, and a case study that juxtaposes the surveillance system in Africa with other countries.
## Machine Learning Models
Machine Learning algorithms trained using the ATLAS dataset to predict the presence of antimicrobial resistance genes in bacterial samples and also predict the resistance status based on a complex network of sample metadata and specific subsidiary data as input parameters. The models' performance, accuracy, and efficiency are also analyzed.
![image](https://github.com/user-attachments/assets/d8901181-1be1-497d-8148-a11d4e18b8fa)

# App Link
Here is the link to the webapp deployed via Streamlit: [PANGEA](https://pangea-amr.streamlit.app/)

# Required Packages
The following packages are imported in the code:
- streamlit==1.37.1
- pandas==2.2.2
- seaborn==0.13.2
- matplotlib==3.9.1
- plotly==5.22.0
- plotly.express==0.4.0
- pybase64==1.4.0
- extra_streamlit_components
- streamlit_option_menu==0.3.13
- numpy==1.26.4
- joblib==1.4.2
- networkx==3.3
- lightgbm==4.5.0
- scikit-learn==1.3.2

# Datasets
The dataset used for this projects is the Pfizer's ATLAS dataset, provided for the project under the 2024 Vivli AMR Open Data Challenge (https://amr.vivli.org/data-challenge/data-challenge-overview/)

# APPLICATION FUNCTIONALITIES
# Explorative Data Analysis
Heatmaps were generated to display the prevalence of AMR genes across different bacterial species, categorized by gene classes. Bar plots were used to depict the distribution of genotypic data across continents, highlighting regions with significant recorded isolates. Sankey diagrams illustrated the relationships between bacteria, gene classes, genes, and strains, offering an intuitive view of how these elements are interconnected. Jaccard similarity heatmaps were created to visualize the co-occurrence of genes within selected bacterial isolates. Additionally, global and continental distribution of genotypic data by species was mapped, providing insights into which species and genotypes are most common worldwide and in specific regions. An interactive world map was developed to highlight geographical hotspots for particular genotypes, giving a global perspective on the distribution and spread of AMR genes. Time series visualizations were employed to compare genetic data trends across continents over time, using line plots to contrast regional trends against the global average. Finally, genotype network analysis explored the relationships between AMR genes, bacterial species, and their geographic distribution, revealing key clusters of closely associated genes and species.
![image](https://github.com/user-attachments/assets/8fa39ef5-9cf9-4c8c-ad2a-649610b63505)
![newplot](https://github.com/user-attachments/assets/9f5dcff5-42b1-4f91-aef0-da0836a134ca)
![all](https://github.com/user-attachments/assets/40d4ff2e-1e1d-43b4-b774-b7b642e49d12)

# Comparative Analysis
Key variables analysed included country, resistance status (categorized as Intermediate, Resistant, or Susceptible), MIC, and relevant clinical and demographic factors. Horizontal bar plots were generated to visualize the distribution of resistance status across different African countries. To further explore the relationship between MIC values and country of origin, a linear regression model was employed. This model controlled for the resistance status of the isolates, enabling an examination of how MIC values vary across countries while accounting for whether isolates are intermediate, resistant, or susceptible.
![Afr_others2](https://github.com/user-attachments/assets/ff0fd351-428d-4bb0-8651-b02904580dfc)

# Machine Learning
Machine learning approaches were implemented to predict resistance gene profiles and MIC values. For gene prediction, metadata was combined with AMR status and corresponding MIC values. A Random Forest model was trained to predict the presence or absence of specific resistance genes based on the antibiotic resistance profiles and MIC values. In parallel, a LightGBM model was developed to predict the resistance status of antibiotics, leveraging both the metadata and the gene profiles as input variables.
![image](https://github.com/user-attachments/assets/b435019b-8b83-4143-b8bd-89ac62f48e3a)

# **Authors**
Developed by Agboeze Tochukwu, Daramola Oluwasegun, Akomolafe Ayobami, and Adedeji Roqeeb, using the Pfizer's ATLAS dataset as part of the 2024 Vivli AMR Open Data Challenge.



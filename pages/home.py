from typing import List, Tuple
import streamlit as st
import pandas as pd


#st.image("cover.png",
    #        use_column_width=True)
pangea = """
    <div style="background-color:#275d5d;padding:4px">
    <h1 style='text-align: center; color: white; font-size: 120px;'>PANGEA</h1>
    </div>
    """
st.markdown(pangea, unsafe_allow_html=True)
#st.markdown("<h1 style='text-align: center; color: gray; font-size: 120px;'>PANGEA</h1>", unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; color: gray; font-size: 20px;'>Predictive Analytics and Genotypic Evaluation for AMR in Africa</h1>", unsafe_allow_html=True)
st.markdown("<div align='center'><br>"
            "<img src='https://img.shields.io/badge/MADE%20WITH-Python%20-red?style=for-the-badge'"
            "alt='API stability' height='28'/>"
            "<img src='https://img.shields.io/badge/ANALYSIS%20WITH-RStudio%20-blue?style=for-the-badge'"
            "alt='API stability' height='20'/>"
            "<img src='https://img.shields.io/badge/DASHBOARDING%20WITH-Streamlit-brown?style=for-the-badge'"
            "alt='API stability' height='28'/></div>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1.2, 1.2, 1.3])
with col1:
    st.markdown("<h1 style='text-align: center; color: black; font-size: 30px;'>Explorative Data Analysis</h1>", unsafe_allow_html=True)
    st.markdown(
    """
    <div style="text-align: justify;">
    Interact with the insightful visualisations that provide detailed explorative data summaries of the ATLAS dataset, with visualisations ranging from AMR determinant genes theme-focused to global-scale data summaries.
    </div>
    """,
    unsafe_allow_html=True
    )
    st.write("")
    if st.button("Go to the Explorative Data Analysis page", type="primary", key="EDA"):
        st.switch_page("pages/visualisation.py")

with col2:
    st.markdown("<h1 style='text-align: center; color: black; font-size: 30px;'>Comparative Analysis</h1>", unsafe_allow_html=True)
    st.markdown(
    """
    <div style="text-align: justify;">
    Engage the comparative analyses conducted to identify predictors of poor AMR stewardship in Africa and pain points in the existing data for the surveillance work in Africa. This details a comparative markdown detailing statistical inference of data comparism, and a case study that juxtaposes the surveillance system in Africa with other countries. 
   </div>""",
    unsafe_allow_html=True
    )
    st.write("")
    if st.button("Go to the Comparative Analysis page", type="primary", key="CA"):
        st.switch_page("pages/analysis.py")

with col3:
    st.markdown("<h1 style='text-align: center; color: black; font-size: 30px;'>Machine Learning</h1>", unsafe_allow_html=True)
    st.markdown(
    """
    <div style="text-align: justify;">
        Interact with 2 Machine Learning algorithms trained using the ATLAS dataset to predict the presence of antimicrobial resistance genes in bacterial samples and also predict the resistance status based on a complex network of sample metadata and specific subsidiary data as input parameters. The models' performance, accuracy, and efficiency are also analyzed.
    </div>
    """,
    unsafe_allow_html=True
    )    
    st.write("")
    if st.button("Go to the Machine Learning page", type="primary", key="ML"):
        st.switch_page("pages/ml.py")

st.divider()
col1, col2 = st.columns([1, 7])

with col1:
    prob_stat = """
        <div style="background-color:#275d5d;padding:4px">
        <h1 style='text-align: center; color: white; font-size: 18px;'>Problem Statement</h1>
        </div>
        """
    st.markdown(prob_stat, unsafe_allow_html=True)
with col2:
    st.markdown('''
                Traditional methods like antimicrobial susceptibility testing (AST), mainly used 
                for AMR surveillance in Africa, need more details on resistance mechanisms and are 
                inefficient in the early detection of pathogenic outbreaks. Next-generation 
                sequencing (NGS) offers a more precise view, but its high cost limits its use in 
                the continent. This necessitates innovative solutions for addressing the challenges 
                of African countries in tackling AMR.
                ''')

with st.sidebar:
    st.info("""Developed by **Agboeze Tochukwu, Daramola Oluwasegun, Akomolafe Ayobami,** and **Adedeji Roqeeb** using Pfizer's
            ATLAS dataset as part of the [Vivli AMR Data Challenge 2024](https://amr.vivli.org/breaking-news-vivli-announces-the-2024-amr-surveillance-data-challenge/).""")
    st.markdown('''[![Github Repo](https://badgen.net/badge/icon/GitHub?icon=github&label)](https://github.com/OluwasegunIsaac/pangea)''')
    st.markdown("<br>",unsafe_allow_html=True)


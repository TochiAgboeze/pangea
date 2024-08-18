
import streamlit as st


st.set_page_config(layout="wide")

# --- PAGE SETUP ---
home = st.Page(page= "pages/home.py", title="Home", icon=":material/home:", default=True)
viz = st.Page(page= "pages/visualisation.py", title="Explorative Data Analysis", icon=":material/bar_chart:")
analysis = st.Page(page= "pages/analysis.py", title="Comparative Analysis", icon=":material/analytics:")
ml = st.Page(page= "pages/ml.py", title="Machine Learning", icon=":material/data_table:")


# --- NAVIGATION SETUP ---
pg = st.navigation(pages=[home, viz, analysis, ml])

# --- COMMON TO ALL PAGES ---
#st.logo("assets/xxx.png")

pg.run()

import streamlit as st
import base64
from streamlit_option_menu import option_menu
import extra_streamlit_components as stx
import pandas as pd

if 'currentStep' not in st.session_state:
    st.session_state.currentStep = 0

currentStep = st.session_state.currentStep
currentStep = stx.stepper_bar(steps=["Comparative Phenotypic Distribution", "Comparative Statistical Analysis", "Comparative Spotlight"], lock_sequence=False)

if currentStep == 0:
    with st.expander("Comparative Analysis 1 & 2 - Markdown"):
        st.markdown('''
            * _Phenotypic differences of the MIC and resistance status between Africa and Non-African countries._
        ''')
    col1, col2 = st.columns(2)
    with col1:
        st.image('assets/Afr_others.png', output_format='png', use_column_width=True)
    with col2:
        st.image('assets/Afr_others2.png', output_format='png', use_column_width=True)

    st.divider()

    with st.expander("Comparative Analysis 3 - Markdown"):
        st.markdown('''
            * _Phenotypic differences between Africa and Non-African countries._
        ''')
    st.image('assets/EDA.png', output_format='png', use_column_width=True)


if currentStep == 1:
    st.markdown("<h1 style='text-align: center;'>Statistical Analysis on the predictors of AMR in Africa</h1>", unsafe_allow_html=True)
    st.divider()
    st.markdown("<h4 style='text-align: center;'>Regression Model and Analysis of Variance(ANOVA)</h4>", unsafe_allow_html=True)
    st.markdown('''
                A linear regression model was used to explore more factors influencing antimicrobial resistance, with MIC as the dependent 
                variable and country, antibiotic type, and bacterial species as independent variables. The residual standard error was 15.14, 
                indicating the average deviation of observed MIC values from those predicted by the model. 
                ''')
    data = {'Metric': ['Residual standard error','Degrees of freedom','Multiple R-squared', 'Adjusted R-squared','F-statistic',
                       'F-statistic DF', 'p-value'],
                       'Value': [15.14, 329918, 0.2464, 0.246, 596.1,'181 and 329918','< 2.2e-16']}

    rs_error = pd.DataFrame(data)
    st.dataframe(rs_error, use_container_width=True, hide_index=True)

    st.markdown('''
                The model achieved a multiple R² value of .2464, indicating that approximately 24.64% of the variance in MIC values is 
                explained by the predictors. ANOVA results showed that MIC values are significantly influenced by antibiotic type, F(39, 329918) 
                = 1861.14, p < .001, country, F(12, 329918) = 405.55, p < .001, and bacterial species, F(130, 329918) = 234.22, p < .001. 
                The overall F-statistic, F(181, 329918) = 596.1, p < .001, confirms that these predictors collectively explain a substantial 
                portion of the variance in MIC values.
                ''')
    data = {
    'Source': ['Country', 'Antibiotics', 'Species', 'Residuals'],
    'Df': [12, 39, 130, 329918],
    'Sum Sq': [1115380, 16635623, 6978427, 75613750],
    'Mean Sq': [92948, 426554, 53680, 229],
    'F value': [405.55, 1861.14, 234.22, None],
    'Pr(>F)': ['< 2.2e-16', '< 2.2e-16', '< 2.2e-16', None],
    'Significance': ['***', '***', '***', '']}

    anova = pd.DataFrame(data)
    st.dataframe(anova, use_container_width=True, hide_index=True)
    st.markdown("<h6 style='text-align: center;'>Statistical Inference</h6>", unsafe_allow_html=True)
    st.markdown('''
                Strong evidence is presented by the statistical analyses indicating that the type of antibiotic, the country, and the species 
                of bacteria are important determinants of antimicrobial resistance trends in Africa. The chi-square test results suggest that 
                public health strategies must be geographically tailored, considering the variability in resistance patterns across regions. 
                The regression model and ANOVA findings further emphasize the importance of these factors in determining MIC values, which has 
                direct implications for the development of predictive models aimed at enhancing AMR surveillance and guiding clinical 
                decision-making.
                ''')
    st.markdown("<h4 style='text-align: center;'>Chi-Square Test of Independence</h4>", unsafe_allow_html=True)
    st.markdown('''
                A Pearson's chi-square test revealed a significant association between country and antimicrobial resistance status 
                (Intermediate, Resistant, Susceptible).
                ''')
    
    data = {
    'Test': ["Pearson's Chi-squared"], 'X-squared': [8782.4], 'Df': [24],'p-value': ['< 2.2e-16']}

    chi = pd.DataFrame(data)
    st.dataframe(chi, use_container_width=True, hide_index=True)
    st.markdown('''
                The substantial chi-square statistic suggests a notable divergence between the observed and expected frequencies under 
                the assumption of independence, implying that the distribution of resistance statuses is not uniform across the African 
                countries analyzed. This finding is critical, as it underscores regional disparities in antimicrobial resistance patterns, 
                which are essential for tailoring public health interventions. The significant p-value further reinforces the importance of 
                considering geographical factors in the design of AMR surveillance and intervention strategies.
                ''')
    st.divider()
    st.markdown("<h3 style='text-align: center;'>Africa vs Other countries</h3>", unsafe_allow_html=True)
    st. markdown('''
                 A Pearson's chi-square test was conducted to examine the relationship between geographic region (Africa vs. Others) and 
                 antimicrobial resistance status (Intermediate, Resistant, and Susceptible). The results were significant, χ²(2, N = 353,034) 
                 = 2859.5, p < .001, suggesting that the distribution of antimicrobial resistance status differs significantly between African 
                 regions and other parts of the world. This indicates that regional factors may play a crucial role in the prevalence and 
                 patterns of antimicrobial resistance.
                 ''')
    data = {
    'Region': ['Africa', 'Others'],
    'Intermediate': [25077, 11675],
    'Resistant': [78311, 37240],
    'Susceptible': [226712, 151019]}

    conting = pd.DataFrame(data)
    st.dataframe(conting, use_container_width=True, hide_index=True)

    st.markdown('''
                The linear regression model reported a residual standard error of 15.01 with 529,716 degrees of freedom. The multiple R-squared 
                was 0.2242, with an adjusted R-squared of 0.2237, indicating that the model explains approximately 22.37% of the variance in 
                MIC values. The F-statistic was significant, F(317, 529716) = 482.8, p < 2.2e-16, confirming the model's overall predictive strength.
                ''')
    data = {
    'Statistic': ['X-squared', 'df', 'p-value'], 'Value': [2859.5, 2, '< 2.2e-16']}

# Create the DataFrame
    chi_others = pd.DataFrame(data)
    st.dataframe(chi_others, use_container_width=True, hide_index=True)

    st.markdown('''
                These findings suggest that group, antibiotic type, and bacterial species are all critical factors influencing MIC values, 
                each contributing significantly to the model’s explanatory power
                ''')

if currentStep == 2:
    st.markdown("<h1 style='text-align: center;'>Comparative Pathogen Spotlight</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center;'>Escherichia coli and Staphylococcus aureus in Africa - a Case Study</h4>", unsafe_allow_html=True)
    st.divider()
    st.markdown('''
                A study conducted in 2019 by the [Antimicrobial Resistance Collaborators](https://doi.org/10.1016/S0140-6736(21)02724-0)
                estimated deaths attributable to and associated with bacterial AMR for 23 pathogens and 88 pathogen–drug combinations 
                in 204 countries. They reported the following findings:
                ''')
    col1, col2 = st.columns(2)
    with col1:
        st.write("**All-age rate of deaths attributable to and associated with AMR by region**")
        st.image('assets/death_by_region.jpg', output_format='jpg', use_column_width=True)
    with col2:
        st.write("**Global deaths (counts) attributable to and associated with AMR by pathogen**")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.image('assets/death_by_pathogen.jpg', output_format='jpg', use_column_width=True)
    
    st.markdown('''
                Sub-Saharan Africa is particularly vulnerable to the impacts of AMR, with the highest death 
                rates per 100,000 population in Western and Eastern Sub-Saharan Africa. The pathogens Escherichia coli, 
                Staphylococcus aureus, and Klebsiella pneumoniae are the leading causes of death, highlighting the urgent 
                need for effective interventions and AMR management strategies in these regions.
            ''')
    _,col1,_ = st.columns([1,2.7,1])
    with col1:
        st.image('assets/perc_prev.png', output_format='png', use_column_width=True)
    st.markdown('''
                According to the Pfizer's ATLAS dataset, **Escherichia coli**, Klebsiella pneumoniae, and Acinetobacter baumannii 
                are more prevalent in Africa, suggesting a higher burden of these pathogens, which could be due to various factors. 
                However, **Staphylococcus aureus** and Streptococcus pneumoniae are more prevalent in non-African region.
                ''')
    st.markdown("<h5 style='text-align: center;'>A comparison between two organism of differing prevalence in Africa under Pfizer's ATLAS:</h5>", unsafe_allow_html=True)
    
    col1, _, col2 = st.columns([5,0.1,5])
    with col1:
        ecoli = """
        <div style="background-color:#EFB5B5;padding:3.5px">
        <h6 style="color:black;text-align:center;"> Escherichia coli in Africa (Higher) </h6>
        </div>
        """
        st.markdown(ecoli, unsafe_allow_html=True)
        st.write('''
                 Escherichia coli O157:H7 is an important food-borne and water-borne pathogen that causes 
                 hemorrhagic colitis and the hemolytic-uremic syndrome in humans and may cause serious morbidity 
                 and large outbreaks worldwide [Gambushe et. al., 2024](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9420067/). 
                 Infections with diarrheagenic E. coli are likewise more frequent in African countries, mostly in Ethiopia, 
                 Nigeria, and South Africa.
                 ''')
        st.image('assets/Ecoli.png', output_format='png', use_column_width=True)
        st.markdown('''
                    Various investigations in the African continent have detected and reported resistance to various 
                    antimicrobial agents of STEC O157:H7. Generally, the control and prudent use of antimicrobials are 
                    largely unregulated in the majority of developing countries, including African countries
                    ''')
    
    with col2:
        saureus = """
        <div style="background-color:#B9E4B4;padding:3.5px">
        <h6 style="color:black;text-align:center;"> Staphylococcus aureus in Africa (Lower) </h6>
        </div>
        """
        st.markdown(saureus, unsafe_allow_html=True)
        st.write('''
                 Staphylococcus aureus is a major human pathogen that causes a wide range of clinical infections, 
                 such as bacteremia and infective endocarditis [Schaumburg et. al., 2014](https://doi.org/10.1111/1469-0691.12690). 
                 As in other parts of the world, there is wide diversity among S. aureus lineages colonizing and infecting the 
                 African population.
                 ''')
        st.image('assets/Saureus.png', output_format='png', use_column_width=True)
        st.markdown('''
                    Studies have revealed a higher incidence of S. aureus infection in Africa than in 
                    industrialized countries. The annual incidence of S. aureus bacteraemia was 3.28 cases per 1000 hospital 
                    admissions (South Africa), with the highest incidence in children aged <5 years. For comparison, 
                    the annual incidence rates in the USA were 2.3 cases per 100 000 person-years for MSSA and 1.5 cases per 100 000 person-years for MRSA.
                    ''')
    st.markdown("<h5 style='text-align: center;'>Comparative Inference</h5>", unsafe_allow_html=True)
    con = st.container(border=True)
    con.markdown('''
                The severity of the AMR epidemic in Africa is currently dampened by low surveillance in the region.
                The observed lower percentage prevalence of S. aureus and S. pneumonia in Africa is inaccurate and 
                reflective of the low surveillance focused on thEse organisms in Africa. Research on African S. aureus 
                has been largely neglected in the past, which has a significant impact on the recorded data of this pathogen. 
                S. aureus, Streptococcus pneumoniae (which is also recorded lower in the ATLAS dataset) or extended-spectrum 
                β-lactamase-producing Enterobacteriaceae is high in Africa.
                ''')
    con.markdown("<h6 style='text-align: justify;'>The challenge for a more accurate surveillance system in Africa contributes largely to exemption of the inherent presence of the epidemic. More focus should be directed at better and improved surveillance to foster public acknowledgement of the problem, which has the potential to yield a more effective stewardship approach:</h6>", 
                 unsafe_allow_html=True)

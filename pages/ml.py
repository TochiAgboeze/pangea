import streamlit as st
import pandas as pd
import extra_streamlit_components as stx
import numpy as np
import os
import pickle
import joblib
import plotly.express as px
import warnings
import lightgbm
from sklearn.ensemble import RandomForestClassifier
warnings.filterwarnings("ignore")



Species = ['Pseudomonas aeruginosa', 'Serratia marcescens', 'Acinetobacter pitii', \
           'Acinetobacter baumannii', 'Enterobacter cloacae', 'Escherichia coli', \
           'Haemophilus influenzae', 'Staphylococcus aureus', 'Enterococcus faecium', \
           'Enterococcus faecalis', 'Streptococcus agalactiae', 'Klebsiella pneumoniae', \
           'Klebsiella aerogenes', 'Acinetobacter junii', 'Klebsiella oxytoca', 'Enterobacter kobei', \
           'Streptococcus pneumoniae', 'Acinetobacter, non-speciated', 'Acinetobacter lwoffii', \
           'Serratia liquefaciens', 'Enterobacter asburiae', 'Citrobacter freundii', 'Serratia fonticola', \
           'Serratia rubidaea', 'Acinetobacter schindleri', 'Acinetobacter guillouiae', 'Clostridium perfringens', \
           'Clostridioides difficile', 'Clostridium tertium', 'Clostridium butyricum', 'Clostridium hathewayi', \
           'Clostridium barati', 'Bacteroides fragilis', 'Parabacteroides distasonis', 'Bacteroides nordii', \
           'Prevotella denticola', 'Bacteroides vulgatus', 'Bacteroides thetaiotaomicron', 'Bacteroides uniformis', \
           'Prevotella buccae', 'Prevotella oris', 'Prevotella bivia', 'Peptostreptococcus anaerobius', \
           'Stenotrophomonas maltophilia', 'Lelliottia amnigena', 'Acinetobacter calcoaceticus', \
           'Acinetobacter nosocomialis', 'Enterococcus, non-speciated', 'Pluralibacter gergoviae', \
           'Acinetobacter radioresistens', 'Acinetobacter johnsonii', 'Enterococcus avium', \
           'Staphylococcus haemolyticus', 'Acinetobacter ursingii', 'Acinetobacter haemolyticus', \
           'Enterococcus raffinosus', 'Staphylococcus epidermidis', 'Enterococcus casseliflavus', 'Enterococcus hirae', \
           'Serratia odorifera', 'Enterococcus gallinarum', 'Staphylococcus hominis', 'Staphylococcus lugdunensis', \
           'Staphylococcus simulans', 'Proteus vulgaris', 'Citrobacter koseri', 'Morganella morganii', \
           'Providencia stuartii', 'Streptococcus bovis', 'Moraxella catarrhalis', 'Streptococcus pyogenes', \
           'Proteus mirabilis', 'Staphylococcus saprophyticus', 'Streptococcus constellatus', 'Haemophilus parainfluenzae', \
           'Streptococcus dysgalactiae', 'Streptococcus anginosus', 'Streptococcus gallolyticus', 'Streptococcus sanguinis', \
            'Staphylococcus warneri', 'Aeromonas caviae', 'Citrobacter braakii', 'Enterobacter ludwigii', \
            'Acinetobacter parvus', 'Acinetobacter tjernbergiae', 'Klebsiella, non-speciated', 'Serratia, non-speciated', \
            'Serratia ficaria', 'Enterobacter, non-speciated', 'Klebsiella ozaenae', 'Peptostreptococcus magnus', \
            'Parvimonas micra', 'Anaerococcus tetradius', 'Prevotella loescheii', 'Bacteroides ovatus', \
            'Clostridium clostridiiformis', 'Prevotella oralis', 'Clostridium subterminale', 'Prevotella intermedia', \
            'Clostridium ramosum', 'Bacteroides caccae', 'Campylobacter ureolyticus', 'Clostridium paraputrificum', \
            'Anaerococcus prevotii', 'Clostridium limosum', 'Streptococcus castoreus', 'Providencia rettgeri', \
            'Staphylococcus capitis', 'Citrobacter farmeri', 'Enterobacter cancerogenus', 'Pseudomonas putida', \
            'Citrobacter gillenii', 'Citrobacter murliniae', 'Klebsiella variicola', 'Haemophilus parahaemolyticus', \
            'Streptococcus, viridans group', 'Serratia ureilytica', 'Streptococcus oralis', 'Acinetobacter baylyi', \
            'Enterobacter agglomerans', 'Pseudomonas nitroreducens', 'Citrobacter sedlakii', 'Prevotella buccalis', \
            'Peptostreptococcus hydrogenalis', 'Bacteroides salersyae', 'Bacteroides massiliensis', 'Prevotella nanceinsis', \
            'Prevotella nigrescens', 'Parabacteroides goldsteinii', 'Anaerococcus lactolyticus', 'Peptoniphilus harei', \
            'Prevotella melaninogenica', 'Clostridium aldenense', 'Prevotella disiens', 'Clostridium citroniae', \
            'Peptoniphilus gorbachii', 'Clostridium innocuum', 'Clostridium scindens', 'Streptococcus salivarius', \
            'Raoultella ornithinolytica', 'Raoultella planticola', 'Enterococcus durans', 'Staphylococcus cohnii', \
            'Clostridium septicum', 'Clostridium sporogenes', 'Clostridium sordellii', 'Enterobacter sakazakii', \
            'Staphylococcus sciuri', 'Serratia plymuthica', 'Hafnia alvei', 'Clostridium celerecrescens', \
            'Anaerococcus hydrogenalis', 'Anaerococcus vaginalis', 'Bacteroides pyogenes', 'Prevotella baroniae', \
            'Bacteroides intestinalis', 'Prevotella histicola', 'Anaerococcus murdochii', 'Clostridium symbiosum', \
            'Bacteroides stercosis', 'Peptoniphilus indolicus', 'Prevotella spp', 'Prevotella pallens', \
            'Prevotella bergensis', 'Prevotella salivae', 'Prevotella maculosa', 'Citrobacter amalonaticus', \
            'Citrobacter, non-speciated', 'Staphylococcus caprae', 'Neisseria gonorrhoeae', 'Proteus penneri', \
            'Streptococcus mitis', 'Pseudomonas monteilii', 'Proteus hauseri', 'Streptococcus intermedius', \
            'Staphylococcus pseudointermedius', 'Pantoea agglomerans', 'Pseudomonas stutzeri', 'Anaerococcus spp', \
            'Clostridium sphenoides', 'Parabacteroides johnsonii', 'Staphylococcus schleiferi', 'Clostridium cadaveris', \
            'Staphylococcus auricularis', 'Providencia alcalifaciens', 'Streptococcus parasanguinis', 'Enterobacter hormaechi', \
            'Escherichia hermanii', 'Providencia, non-speciated', 'Raoultella terrigena', 'Burkholderia cepacia', \
            'Streptococcus sanguis', 'Staphylococcus pasteuri', 'Staphylococcus Coagulase Negative', 'Serratia grimesii', \
            'Acinetobacter towneri', 'Streptococcus suis', 'Staphylococcus xylosus', 'Pseudomonas alcaliphila', \
            'Klebsiella ornithinolytica', 'Proteus rettgeri', 'Peptoniphilus spp', 'Clostridium spp', 'Clostridium bifermentans', \
            'Pseudomonas otitidis', 'Bacteroides spp', 'Clostridium bolteae', 'Anaerococcus octavius', 'Prevotella corporis', \
            'Clostridium disporicum', 'Clostridium histolyticum', 'Clostridium beijerinckii', 'Clostridium glycolicum', \
            'Prevotella oulorum', 'Clostridium cochlearium', 'Staphylococcus intermedius', 'Enterobacter intermedium', \
            'Klebsiella planticola', 'Burkholderia cenocepacia', 'Bacteroides coagulans', 'Bacteroides cellulosilyticus', \
            'Prevotella heparinolytica', 'Acinetobacter anitratus', 'Cronobacter sakazakii', 'Streptococcus canis', \
            'Staphylococcus pettenkoferi', 'Pseudomonas mendocina', 'Aeromonas hydrophila', 'Pantoea septica', \
            'Streptococcus lutetiensis', 'Citrobacter youngae', 'Peptostreptococcus spp', 'Finegoldia magna', \
            'Aeromonas veronii', 'Pseudomonas mosselii', 'Bacteroides faecis', 'Kluyvera ascorbata', 'Enterobacter taylorae', \
            'Prevotella timonensis', 'Peptoniphilus olsenii', 'Bacteroides eggerthii', 'Prevotella veroralis', \
            'Enterobacter gergoviae', 'Peptoniphilus lacrimalis', 'Prevotella amnii', 'Enterococcus mundtii', \
            'Streptococcus massiliensis', 'Clostridium colicanis', 'Acinetobacter bereziniae', 'Staphylococcus spp', \
            'Aeromonas spp', 'Proteus spp', 'Escherichia vulneris', 'Acinetobacter dijkshoorniae', 'Pantoea dispersa', \
            'Pseudomonas pseudoalcaligenes', 'Citrobacter diversus', 'Pseudomonas spp', 'Streptococcus, Beta Hemolytic', \
            'Achromobacter xylosoxidans', 'Acinetobacter seifertii', 'Staphylococcus argenteus', 'Corynebacterium aurimucosum', \
            'Pseudomonas alcaligenes', 'Pseudomonas citronellolis', 'Staphylococcus condimenti', 'Pantoea spp', 'Salmonella spp', \
            'Enterobacter bugandensis', 'Acinetobacter beijerinckii', 'Klebsiella spp', 'Acinetobacter spp', 'Enterobacter spp', \
            'Citrobacter spp', 'Providencia spp', 'Enterobacter xiangfangensis', 'Acinetobacter courvalinii', \
            'Pseudomonas putida/fluorescens Group', 'Bordetella trematum', 'Myroides odoratimimus', 'Achromobacter insolitus', \
            'Acinetobacter proteolyticus', 'Staphylococcus arlettae', 'Pseudomonas fulva', 'Staphylococcus saccharolyticus', \
            'Ochrobactrum anthropi', 'Staphylococcus petrasii', 'Alcaligenes faecalis', 'Cronobacter spp', \
            'Pseudomonas guariconensis', 'Acinetobacter tandoii', 'Bordetella spp', 'Providencia rustigianii', \
            'Pseudomonas graminis', 'Acinetobacter dispersus', 'Acinetobacter variabilis', 'Enterobacter roggenkampii', \
            'Serratia spp', 'Escherichia spp', 'Acinetobacter soli', 'Haemophilus spp', 'Acinetobacter lactucae', \
            'Acinetobacter vivianii', 'Moraxella spp', 'Raoultella spp', 'Enterococcus spp', 'Acinetobacter gyllenbergii', \
            'Streptococcus spp', 'Acidaminococcus fermentans', 'Enterococcus canintestini', 'Enterococcus Group D', \
            'Acinetobacter modestus', 'Morganella spp', 'Acinetobacter venetianus', 'Acinetobacter colistiniresistens', \
            'Acinetobacter indicus', 'Enterocloster clostridioformis', 'Enterocloster citroniae', 'Paraclostridium spp', \
            'Eggerthella lenta', 'Phocaeicola vulgatus', 'Peptoniphilus coxii', 'Parvimonas spp', 'Enterocloster bolteae', \
            'Acinetobacter pseudolwoffii', 'Prevotella jejunii', 'Paraclostridium bifermentans', 'Elizabethkingia anophelis', \
            'Comamonas kerstersii', 'Moraxella osloensis', 'Eggerthella spp', 'Paeniclostridium sordelli', 'Bacteroides capsillosis', \
            'Clostridium novyia', 'Bacteroides bivius', 'Peptoniphilus asaccharolyticus', 'Bacteroides merdeae', \
            'Prevotella tannerae', 'Clostridium hastiforme', 'Fusobacterium nucleatum', 'Anaerovorax spp', 'Clostridium scatalogenes', \
            'Clostridium putrificum', 'Kerstersia gyiorum', 'Enterobacter liquifaciens', 'Enterococcus flavescens', 'Eubacterium lentum', \
            'Peptostreptococcus lactolyticus', 'Bacteroides dorei', 'Prevotella multiformis', 'Bacteroides splanchnicus', \
            'Peptostreptococcus indolicus', 'Eubacterium aerofaciens', 'Veillonella parvula', 'Acinetobacter alcaligenes', \
            'Clostridium rectum', 'Peptostreptococcus tetradius', 'Klebsiella rhinoscleromatis', 'Streptococcus equi', \
            'Haemophilus pittmaniae', 'Staphylococcus vitulinus', 'Escherichia fergusonii', 'Staphylococcus hyicus', \
            'Streptococcus gordonii', 'Pseudomonas fluorescens', 'Enterococcus malodoratus', 'Pseudomonas stewartii']

Family = ['Non-Enterobacteriaceae', 'Enterobacteriaceae', 'Haemophilus spp', 'Staphylococcus spp', \
          'Enterococcus spp', 'Streptococcus spp (no S. pneumo)', 'Streptococcus pneumoniae', \
          'Gram Positive Anaerobes', 'Gram Negative Anaerobes', 'Moraxellaceae', 'Neisseria gonorrhoeae', \
          'Other Gram Positives', 'Non-Enterobacterales', 'Enterobacterales', 'Alicaligenaceae', 'Morganellaceae']

Country = ['France', 'Spain', 'Belgium', 'Italy', 'Germany', 'Canada', 'United States', 'Ireland', 'Portugal', \
           'Israel', 'Greece', 'China', 'United Kingdom', 'Kuwait', 'Poland', 'Switzerland', 'Hungary', 'Austria', \
           'Colombia', 'Chile', 'Finland', 'Australia', 'Mexico', 'Denmark', 'Sweden', 'Hong Kong', 'Japan', \
           'Croatia', 'Malaysia', 'Nigeria', 'Kenya', 'Czech Republic', 'Netherlands', 'Russia', 'Romania', \
           'Venezuela', 'Thailand', 'Philippines', 'Turkey', 'Korea, South', 'South Africa', 'Argentina', 'Taiwan', \
           'Brazil', 'Panama', 'Jordan', 'Saudi Arabia', 'Pakistan', 'Guatemala', 'Morocco', 'India', 'Singapore', \
           'Vietnam', 'Latvia', 'Lithuania', 'Serbia', 'Dominican Republic', 'Costa Rica', 'Ukraine', 'Ivory Coast', \
           'Lebanon', 'New Zealand', 'Qatar', 'Slovenia', 'Cameroon', 'Jamaica', 'Bulgaria', 'Norway', 'Honduras', \
           'Puerto Rico', 'Nicaragua', 'Slovak Republic', 'Oman', 'Malawi', 'Uganda', 'Ghana', 'Namibia', 'Indonesia', \
           'Mauritius', 'Estonia', 'El Salvador', 'Tunisia', 'Egypt']

Gender = ['Male', 'Female']

Age_Group = ['0 to 2 Years', '3 to 12 Years', '13 to 18 Years', '19 to 64 Years', '65 to 84 Years', '85 and Over', 'Unknown']

Speciality = ['Emergency Room', 'Nursing Home / Rehab', 'Medicine General', 'Medicine ICU', 'Surgery General', 'None Given', \
              'Pediatric General', 'Pediatric ICU', 'Clinic / Office', 'Surgery ICU', 'General Unspecified ICU', 'Other']

Source = ['Urine', 'Ear', 'Skin', 'Blood', 'Bronchus', 'Sputum', 'Peritoneal Fluid', 'Bone', 'Wound', 'Placenta', \
          'Gastric Abscess', 'Stomach', 'Vagina', 'Lungs', 'Nose', 'Catheters', 'Exudate', 'Throat', 'CNS: Other', \
          'Peripheral Nerves', 'Eye', 'Decubitus', 'Ulcer', 'Synovial Fluid', 'Genitourinary: Other', 'Tissue Fluid', \
          'Respiratory: Other', 'Trachea', 'Drains', 'Rectum', 'Bile', 'Feces/Stool', 'Skin: Other', 'Bodily Fluids', \
          'Lymph Nodes', 'Spinal Cord', 'Abdominal Fluid', 'None Given', 'Pleural Fluid', 'Aspirate', 'Kidney', \
          'Instruments: Other', 'HEENT: Other', 'Intestinal: Other', 'Mouth', 'Penis', 'Thoracentesis Fluid', \
          'Pancreas', 'Gall Bladder', 'CSF', 'Head', 'Muscle', 'Urethra', 'Liver', 'Brain', 'Burn', 'Nails', \
          'Bone Marrow', 'Respiratory: Sinuses', 'Heart', 'Colon', 'Skeletal: Other', 'Endotracheal aspirate', \
          'Bladder', 'Abscess', 'Bronchoalveolar lavage', 'Circulatory: Other', 'Ureter', 'Appendix', 'Impetiginous lesions', \
          'Furuncle', 'Carbuncle', 'Prostate', 'Uterus', 'Integumentary (Skin Nail Hair)', 'Cellulitis', 'Blood Vessels', \
          'Diverticulum', 'Fallopian Tubes', 'Vas Deferens', 'Spleen', 'Ovary', 'Cervix', 'Lymphatic Fluid', 'Testis', \
          'Hair', 'Esophagus', 'Vomit', 'Thymus', 'Nasopharyngeal Aspirate', 'Transtracheal Aspirate', 'Paracentesis Fluid', \
          'Ascetic Fluid', 'Nasotracheal Aspirate', 'Bronchiole', 'Ileum', 'Pyoderma Lesion']

Patient = ['None Given', 'Inpatient', 'Outpatient', 'Null', 'Other']

Phenotype = ['ESBL', '(BL Neg)', 'MSSA', 'MRSA', '(BL Pos)', 'Null']

Antibiotics = ['Amikacin', 'Amoxycillin clavulanate', 'Ampicillin', 'Cefepime', 'Ceftazidime', 'Ceftriaxone', 'Levofloxacin', \
               'Meropenem', 'Minocycline', 'Piperacillin tazobactam', 'Tigecycline', 'Imipenem', 'Aztreonam', 'Ceftaroline', \
               'Ceftazidime avibactam', 'Doripenem', 'Ertapenem', 'Colistin', 'Ceftolozane tazobactam', 'Ampicillin sulbactam', \
               'Ciprofloxacin', 'Gentamicin', 'Trimethoprim sulfa', 'Meropenem vaborbactam']

status = ['Null', 'Resistant', 'Susceptible', 'Intermediate']

mic = ['4', '>32', '>8', '<=0.06', '2', '0.12', '32', '16', '>16', \
    '1', '8', '0.5', '<=1', '0.25', '>128', '64', '<=0.5', '128', \
    '0.03', '0.06', '<=0.008', '0.015', '>64', '>4', '>1', '<=0.12', \
    '<=0.03', '<=0.015', '<=0.004', '<=0.25', '2.0', '0.008', '1.0', \
    '4.0', '128.0', '8.0000', '2.0000', '32.0000', '4.0000', '0.1200', \
    '16.0000', '64.0000', '0.0600', '0.2500', '0.5000', '1.0000', '128.0000', \
    '0.0300', '<=8', '<=0.002', '0.004']

gene = ['NEG','POS']

Ami_I=Amo_I=Amp_I=Cefe_I=Tige_I=Cefta_I=Ceftr_I=Imi_I=Leno_I=Lin_I=Mero_I=Mino_I=Piper_I=Tige_I=Vanc_I=Ceftar_I=gent=trim=ceftavi=aztavi=azt=ampsul= status


lst=[]
Predictions=[]
def predict_gene(df):
  for i in ["Species", "Family", "Country", "Gender", "Speciality", "Source", "Age Group", "Patient", "Phenotype"]:
    encoder="assets/"+i+".joblib"
    le=joblib.load(encoder)
    df[i]=le.transform(df[i])
  df.replace("Null",-999, inplace=True)
  df.replace("Susceptible", 1, inplace=True)
  df.replace("Resistant", 0, inplace=True)
  df.replace("Intermediate", 2, inplace=True)
  #df.drop(drop, axis=1, inplace=True)
  for i in ['AMPC', 'SHV', 'TEM', 'CTXM1', 'CTXM2', 'CTXM9', 'VEB', 'GES', 'CMY11', 'DHA', 'KPC', 'OXA', 'NDM', 'VIM']:
    name="assets/"+i+".joblib"
    rf=joblib.load(name)
    pred=rf.predict(df.values)
    pred_=rf.predict_proba(df.values)
    lst.append(pred_[0])
    Predictions.append(pred[0])
  s=['AMPC', 'SHV', 'TEM', 'CTXM1', 'CTXM2', 'CTXM9', 'VEB', 'GES', 'CMY11', 'DHA', 'KPC', 'OXA', 'NDM', 'VIM']
  df2=pd.DataFrame(lst)
  df2["Genes"]=s
  df2.rename(columns={0:"NEG", 1:"POS"}, inplace=True)
  fig=px.bar(
  data_frame = df2,
  x = "Genes",
  y = ["NEG","POS"],
  opacity = 0.9,
  orientation = "v",
  barmode = 'group',
  title="Percentage Possibility of Individual AMR determinant gene presence in queried Isolate")

  return fig

def Predict_MIC(df):
  df['Gender'].fillna('Male', inplace=True)
  df['Patient'].fillna('Inpatient', inplace=True)
  df['Patient']=df['Patient'].str.replace('None Given', 'Other')
  df.replace("NEG", 0, inplace=True)
  df.replace("POS", 1, inplace=True)
  for i in ["Species", "Family", "Country", "Gender", "Speciality", "Source", "Age Group", "Patient", "Antibiotics"]:
    encoder="assets/"+i+".pkl"
    file_ = open(encoder,'rb')
    le = pickle.load(file_)
    df[i]=le.transform(df[i])

  name="assets/status.joblib"
  r=joblib.load(name)
  pred=r.predict(df.values)
  pred_=r.predict_proba(df.values)

  if pred==0:
    value = ("Susceptible")
  elif pred==1:
    value = ("Resistant")
  else:
    value = ("Intermediate")

  fig = px.pie(values=pred_[0], names=["Susceptible", "Resistant", "Intermediate"])
  
  return (value, fig)



if 'currentStep' not in st.session_state:
    st.session_state.currentStep = 0

currentStep = st.session_state.currentStep
currentStep = stx.stepper_bar(steps=["AMR Determinant Gene Prediction", "Resistance status Prediction", "Model Performance"], lock_sequence=False)

if currentStep == 0:
    st.write('''
            ###### AMR Determinant Gene Prediction Machine Learning model is trained using the ATLAS dataset to identify and predict the presence of antimicrobial resistance genes in bacterial/pathogen samples based on a complex network of sample metadata, antibiotics susceptibility testing outcome and MIC report as input parameters. ######
                ''')
    patient_meta = """
    <div style="background-color:#65615D;padding:5px">
    <h5 style="color:white;text-align:center;"> Patient Metadata Inputs </h5>
    </div>
    """
    st.markdown(patient_meta, unsafe_allow_html=True)

    with st.form("my_form"):
        #st.markdown('<h2 style="font-size:20px;">NB: Input zero (0) for parameters without values</h1>', unsafe_allow_html=True)
        #st.write("#### **Patient Metadata Inputs**") 
        col1, col2, col3 = st.columns(3)
        with col1:
            species=st.selectbox("Pathogen", Species)
            family=st.selectbox("Pathogen Family class", Family)
            country=st.selectbox("Country of Isolation", Country)
        with col2:
            gender=st.selectbox("Patient Gender", Gender)
            age_group=st.selectbox("Patient Age", Age_Group)
            speciality=st.selectbox("Patient Admission Specialty", Speciality)
        with col3:
            source=st.selectbox("Source of Isolate Isolation", Source)
            patient=st.selectbox("Class of Patient", Patient)
            phenotype=st.selectbox("Antibiotic Phenotype", Phenotype)
        antibiotics_meta = """
        <div style="background-color:#65615D;padding:5px">
        <h5 style="color:white;text-align:center;"> Available Antibiotics Status and MIC Inputs </h5>
        </div>
        """
        st.markdown(antibiotics_meta, unsafe_allow_html=True) 
        
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            ami_I=st.selectbox("Amikacin", Ami_I)
            ami = st.number_input("MIC value")
            st.divider()
            amo_I=st.selectbox("Amoxycillin cluvalunate", Amo_I, key='amo_I')
            amo = st.number_input("MIC value", key='amo')
            st.divider()
            amp_I=st.selectbox("Ampicillin", Amp_I, key='amp_I')
            amp = st.number_input("MIC value", key='amp')
            
        with col2:
            cefe_I=st.selectbox("Cefepime", Cefe_I, key='cefe_I')
            cefe = st.number_input("MIC value", key='cefe')
            st.divider()
            ceftar_I=st.selectbox("Ceftaroline", Ceftar_I, key='ceftar_I')
            ceftar = st.number_input("MIC value", key='ceftar')
            st.divider()
            cefta_I=st.selectbox("Ceftazidime", Cefta_I, key='cefta_I')
            cefta = st.number_input("MIC value", key='cefta')
            
        with col3:
            ceftr_I=st.selectbox("Ceftriaxone", Ceftr_I, key='ceftr_I')
            ceftr = st.number_input("MIC value", key='ceftr')
            st.divider()
            imi_I=st.selectbox("Imipenem", Imi_I, key='imi_I')
            imi = st.number_input("MIC value", key='imi')
            st.divider()
            levo_I=st.selectbox("Levofloxacin", Leno_I, key='levo_I')
            levo = st.number_input("MIC value", key='levo')
                    
        with col4:
            lin_I=st.selectbox("Linezolid", Lin_I, key='lin_I')
            lin = st.number_input("MIC value", key='lin')
            st.divider()
            mero_I=st.selectbox("Meropenem", Mero_I, key='mero_I')
            mero = st.number_input("MIC value", key='mero')
            st.divider()
            mino_I=st.selectbox("Minocycline", Mino_I, key='mino_I')
            mino = st.number_input("MIC value", key='mino')
            
        with col5:
            piper_I=st.selectbox("Piperacillin tazobactam", Piper_I, key='piper_I')
            piper = st.number_input("MIC value", key='piper')
            st.divider()
            tige_I=st.selectbox("Tigecycline", Tige_I, key='tige_I')
            tige = st.number_input("MIC value", key='tige')
            st.divider()
            vanc_I=st.selectbox("Vancomycin", Vanc_I, key='vanc_I')
            vanc = st.number_input("MIC value", key='vanc')

        st.divider()
        col1, col2, col3 = st.columns(3) 
        with col1:    
            ampsul = st.number_input("Ampicillin sulbactam MIC value", key='ampsul')
            azt = st.number_input("Aztreonam MIC value", key='azt')
        with col2:
            aztavi = st.number_input("Aztreonam avibactam MIC value", key='aztavi')
            ceftavi = st.number_input("Ceftazidime avibactam MIC value", key='ceftavi')
        with col3:
            gent = st.number_input("Gentamicin MIC value", key='gent')
            trim = st.number_input("Trimethoprim sulfa MIC value", key='trim')

        submitted = st.form_submit_button("Make Prediction", type='primary')
        
        if submitted:
            output = {'Species': species, 'Family': family,'Country': country,
                      'Gender': gender, 'Age Group': age_group, 'Speciality': speciality,
                      'Source': source, 'Patient': patient, 'Phenotype': phenotype,
                      'Amikacin': ami, 'Amikacin_I': ami_I,'Amoxycillin cluvalunate': amo,
                      'Amoxycillin cluvalunate_I': amo_I, 'Ampicillin': amp, 'Ampicillin_I': amp_I,
                      'Cefepime': cefe, 'Cefepime_I': cefe_I, 'Ceftazidime': cefta, 'Ceftazidime_I': cefta_I,
                      'Ceftriaxone': ceftr, 'Ceftriaxone_I': ceftr_I, 'Imipenem': imi, 'Imipenem_I': imi_I,
                      'Levofloxacin': levo, 'Levofloxacin_I': levo_I, 'Linezolid': lin, 'Linezolid_I': lin_I,
                      'Meropenem': mero, 'Meropenem_I': mero_I, 'Minocycline': mino, 'Minocycline_I': mino_I,
                      'Piperacillin tazobactam': piper, 'Piperacillin tazobactam_I': piper_I,
                      'Tigecycline': tige, 'Tigecycline_I': tige_I, 'Vancomycin': vanc, 'Vancomycin_I': vanc_I,
                      'Ampicillin sulbactam': ampsul, 'Aztreonam': azt, 'Aztreonam avibactam': aztavi,
                      'Ceftaroline': ceftar, 'Ceftaroline_I': ceftar_I, 'Ceftazidime avibactam': ceftavi,
                      'Gentamicin': gent, 'Trimethoprim sulfa': trim}
            

            df=pd.DataFrame([output])
            #print(df.columns)
            figure=predict_gene(df)
            genes=['AMPC', 'SHV', 'TEM', 'CTXM1', 'CTXM2', 'CTXM9', 'VEB', 'GES', 'CMY11', 'DHA', 'KPC', 'OXA', 'NDM', 'VIM']
            genes_df=pd.DataFrame({"Genes":genes, "Status":Predictions})
            genes_df.replace(0, "Negative", inplace=True)
            genes_df.replace(1, "Positive", inplace=True)

            with st.expander("### **AMR determinant gene prediction results**"):
                st.dataframe(genes_df, use_container_width=True)
                st.plotly_chart(figure)


if currentStep == 1:
    st.write('''
            ###### Resistance status Prediction Machine Learning model is trained using the ATLAS dataset to identify and predict the resistance status (Resistance/Intermediate/Susceptible) based on a complex network of sample metadata and available AMR Genotypic data as input parameters. ######
                ''')
    patient_meta = """
    <div style="background-color:#5C5247;padding:5px">
    <h5 style="color:white;text-align:center;"> Patient Metadata Inputs </h5>
    </div>
    """
    st.markdown(patient_meta, unsafe_allow_html=True)

    with st.form("my_form"):
        #st.markdown('<h2 style="font-size:20px;">NB: Input zero (0) for parameters without values</h1>', unsafe_allow_html=True)
        #st.write("#### **Patient Metadata Inputs**") 
        col1, col2, col3 = st.columns(3)
        with col1:
            species=st.selectbox("Pathogen", Species)
            family=st.selectbox("Pathogen Family class", Family)
            country=st.selectbox("Country of Isolation", Country)
        with col2:
            gender=st.selectbox("Patient Gender", Gender)
            age_group=st.selectbox("Patient Age", Age_Group)
            speciality=st.selectbox("Patient Admission Specialty", Speciality)
        with col3:
            source=st.selectbox("Source of Isolate Isolation", Source)
            patient=st.selectbox("Class of Patient", Patient)
            antibiotics=st.selectbox("Antibiotics", Antibiotics)
        gene_meta = """
        <div style="background-color:#5C5247;padding:5px">
        <h5 style="color:white;text-align:center;"> Available AMR Genotypic data Inputs </h5>
        </div>
        """
        st.markdown(gene_meta, unsafe_allow_html=True) 

        col1, col2, col3, col4, col5, col6 = st.columns(6)
        with col1:
            acc = st.selectbox("ACC", gene)
            actmir = st.selectbox("ACTMIR", gene)
            ampc = st.selectbox("AMPC", gene)
            cmy11 = st.selectbox("CMY11", gene)
        with col2:
            cmy1mox = st.selectbox("CMY1MOX", gene)
            ctxm1 = st.selectbox("CTXM1", gene)
            ctxm2 = st.selectbox("CTXM2", gene)
            ctxm825 = st.selectbox("CTXM825", gene)
        with col3:
            ctxm9 = st.selectbox("CTXM9", gene)
            dha = st.selectbox("DHA", gene)
            fox = st.selectbox("FOX", gene)
            ges = st.selectbox("GES", gene)
        with col4:
            imp = st.selectbox("IMP", gene)
            kpc = st.selectbox("KPC", gene)
            ndm = st.selectbox("NDM", gene)
            oxa = st.selectbox("OXA", gene)
        with col5:
            per = st.selectbox("PER", gene)
            shv = st.selectbox("SHV", gene)
            spm = st.selectbox("SPM", gene)
            tem = st.selectbox("TEM", gene)
        with col6:
            veb = st.selectbox("VEB", gene)
            vim = st.selectbox("VIM", gene)

        submitted = st.form_submit_button("Make Prediction", type='primary')
        if submitted:
            output = {'ACC': acc, 'ACTMIR': actmir, 'AMPC': ampc, 'CMY11': cmy11, 
                      'CMY1MOX': cmy1mox, 'CTXM1': ctxm1, 'CTXM2': ctxm2, 'CTXM825': ctxm825, 'CTXM9': ctxm9,
                      'DHA': dha, 'FOX': fox, 'GES': ges, 'IMP': imp, 'KPC': kpc, 'NDM': ndm, 
                      'OXA': oxa, 'PER': per, 'SHV': shv, 'SPM': spm, 'TEM': tem, 'VEB': veb, 'VIM': vim,
                      'Species': species, 'Family': family,'Country': country,
                      'Gender': gender, 'Age Group': age_group, 'Speciality': speciality,
                      'Source': source, 'Patient': patient, 'Antibiotics': antibiotics
            }

            df=pd.DataFrame([output])
            value, fig=Predict_MIC(df)
            
            with st.expander("### **AMR status prediction results**"):
                value = st.write("### ", value)
                st.plotly_chart(fig)
                st.markdown('''
                * NB - Pie Chart outputs the percentage probability of queried organism to be Resistant, Susceptible, or Intermediate.
            ''')

if currentStep == 2:
    st.subheader('Model 1 - Random Forest Model Performance and Reliability Scores')
    patient_meta = """
    <div style="background-color:#65615D;padding:5px">
    <h5 style="color:white;text-align:center;"> AMR Determinant Gene Prediction Model </h5>
    </div>
    """
    st.markdown(patient_meta, unsafe_allow_html=True)
    #Model Score
    data = {
    'Gene Model': ['MPC', 'SHV', 'TEM', 'CTXM1', 'CTXM2', 'CTXM9', 'VEB', 'GES', 'CMY11', 'DHA', 'KPC', 'OXA', 'NDM', 'VIM'],
    'Accuracy Score': [0.9634, 0.9674, 0.8076, 0.9172, 0.9879, 0.9405, 0.9965, 0.9945, 0.9740, 0.9797, 0.9838, 0.9818, 0.9912, 0.9852],
    'F1 Score': [0.7032, 0.9601, 0.7802, 0.9340, 0.4354, 0.6365, 0.7511, 0.6329, 0.6418, 0.5302, 0.8876, 0.8953, 0.9120, 0.7617],
    'Inference': [
        'High accuracy but moderate F1 score. The model might be less reliable in detecting some positive instances.',
        'Very high accuracy and F1 score. The model performs well both in overall accuracy and balance between precision and recall.',
        'Moderate accuracy and F1 score. The model has a reasonable performance but is less reliable compared to others.',
        'High accuracy and F1 score. The model is reliable and well-balanced.',
        'Very high accuracy but low F1 score. The model is likely overfitting or performing poorly in terms of precision and recall.',
        'High accuracy with a moderate F1 score. The model has good general performance but might struggle with some positive cases.',
        'Excellent accuracy and good F1 score. The model is both accurate and fairly reliable in balancing precision and recall.',
        'High accuracy and decent F1 score. The model performs well but could improve in balancing precision and recall.',
        'High accuracy with a moderate F1 score. The model is effective but not as balanced as others.',
        'High accuracy but lower F1 score. The model might have good overall performance but struggles with precision and recall balance.',
        'High accuracy and very good F1 score. The model is both accurate and reliable in balancing precision and recall.',
        'High accuracy and very good F1 score. The model performs excellently in terms of both accuracy and balance.',
        'Excellent accuracy and very high F1 score. The model is very reliable and balanced in performance.',
        'High accuracy and good F1 score. The model is generally reliable and performs well across both metrics.'
    ]
}
    # Create a DataFrame
    df = pd.DataFrame(data)

    st.dataframe(df, use_container_width=True, hide_index=True)

    st.divider()
    st.subheader('Model 2 - Light GBM Model Performance and Reliability Scores')
    patient_meta = """
    <div style="background-color:#A3998D;padding:5px">
    <h5 style="color:white;text-align:center;"> Resistance status Prediction Model </h5>
    </div>
    """
    st.markdown(patient_meta, unsafe_allow_html=True)

    # Define model performance data
    data = {
    'Accuracy': [0.81],
    'Inference': ['The Light GBM model has a good accuracy of 81%, indicating that it performs well overall.']
}

    df = pd.DataFrame(data)
    st.dataframe(df, use_container_width=True, hide_index=True)

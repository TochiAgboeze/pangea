import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from streamlit_option_menu import option_menu
import extra_streamlit_components as stx
import networkx as nx
import base64


# Load the dataset
ATLAS_Dataset = pd.read_csv('assets/atlas_2024_genes.csv')

if 'currentStep' not in st.session_state:
    st.session_state.currentStep = 0

currentStep = st.session_state.currentStep
currentStep = stx.stepper_bar(steps=["AMR Genes Explorative Data Summary", "Global Data Summary"], lock_sequence=False)

if currentStep == 0:

    # Sidebar for user inputs
    with st.sidebar:
        st.header("EDA Parameters")
        region_type = st.multiselect('Select Continent', ['Africa','Europe', 'North America','South America','Asia','Oceania'])
        species = st.multiselect('Select Species', ['Pseudomonas aeruginosa', 'Proteus mirabilis','Acinetobacter baumannii', 
                                                    'Klebsiella oxytoca', 'Escherichia coli', 'Enterobacter cloacae', 
                                                    'Klebsiella pneumoniae', 'Serratia marcescens', 'Citrobacter freundii',
                                                   'Providencia stuartii'])
        st.header("Sankey Parameter")
        gene_classes = st.multiselect('Select AMR gene sub-class(es)', ['Carbapenemase', 'Beta-lactamase', 'ESBL', 'AmpC beta-lactamase'])

    #TIME SERIES VISUALIZATION COMPARING THE TREND OF RECORDED GENOTYPIC DATA OF SELECTED CONTINENT(S) WITH THE GLOBAL AVERAGE
    def compare_with_global_average(df, selected_continents=None):

        df_aggregated = df.groupby(['Year', 'Continents']).size().reset_index(name='Count')
        global_avg = df_aggregated.groupby('Year')['Count'].mean().reset_index(name='Global Average')
        df_aggregated = df_aggregated.merge(global_avg, on='Year')

        if selected_continents is not None:
            df_aggregated = df_aggregated[df_aggregated['Continents'].isin(selected_continents) | (df_aggregated['Continents'] == 'Global Average')]

        plt.figure(figsize=(14, 8))
        sns.lineplot(data=df_aggregated, x='Year', y='Count', hue='Continents', style='Continents', markers=True, dashes=False)
        sns.lineplot(data=df_aggregated, x='Year', y='Global Average', color='black', label='Global Average', linestyle='--')

        plt.title('Comparison of Genotypic Data Trends Across Continents with Global Average')
        plt.xlabel('Year')
        plt.ylabel('Number of Records')

        plt.legend(title='Continent', bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.grid(True)
        plt.tight_layout()
        st.pyplot(plt)


    # Function to visualize the prevalence of AMR genes in selected species
    def amr_gene_prevalence(df, species_list):
        gene_class_mapping = {
            'CTXM9': 'ESBL', 'SHV': 'Beta-lactamase', 'CTXM1': 'ESBL', 'TEM': 'Beta-lactamase', 
            'KPC': 'Carbapenemase', 'AMPC': 'AmpC beta-lactamase', 'ACTMIR': 'AmpC beta-lactamase', 
            'VIM': 'Carbapenemase', 'OXA': 'Carbapenemase', 'CTXM2': 'ESBL', 'VEB': 'ESBL', 
            'CMY11': 'AmpC beta-lactamase', 'DHA': 'AmpC beta-lactamase', 'GES': 'Carbapenemase', 
            'ACC': 'AmpC beta-lactamase', 'CTXM825': 'ESBL', 'NDM': 'Carbapenemase', 'IMP': 'Carbapenemase', 
            'FOX': 'AmpC beta-lactamase', 'SPM': 'Carbapenemase', 'CMY1MOX': 'AmpC beta-lactamase','PER':'ESBL'
        }

        df_filtered = df[df['Species'].isin(species_list)]

        if df_filtered.empty:
            st.warning("No data available for the selected filters.")
            

        pivot_table = df_filtered.pivot_table(index='Gene', columns='Species', aggfunc='size', fill_value=0)
        pivot_table['Gene Class'] = pivot_table.index.map(gene_class_mapping).fillna('Unknown')

        if pivot_table.empty:
            st.warning("No data available for the selected filters.")
           
        class_colors = {'ESBL': 'skyblue', 'Carbapenemase': 'lightgreen','AmpC beta-lactamase': 'lightcoral','Beta-lactamase': 'grey'}
        gene_classes = pivot_table['Gene Class']
        row_colors = gene_classes.map(class_colors)
        pivot_table = pivot_table.drop(columns=['Gene Class'])

        plt.figure(figsize=(12, 8))
        sns.heatmap(pivot_table, cmap="Blues", annot=True, fmt="d", cbar_kws={'label': 'Prevalence'})
        ax = plt.gca()
        for label, color in zip(ax.get_yticklabels(), row_colors):
            label.set_color(color)

        handles = [plt.Line2D([0], [0], color=color, lw=4) for color in class_colors.values()]
        labels = class_colors.keys()
        plt.legend(handles, labels, title='Genotype Subclasses', loc='upper right', bbox_to_anchor=(1.5, 1))
        plt.title(f'Prevalence of AMR Genes by Species')
        plt.xlabel('Species')
        plt.ylabel('Gene')
        
        st.pyplot(plt)
    

    # HEATMAPS DEPICTING THE CO-OCCURENCE OF GENOTYPES FOR SELECTED ISOLATES (JACCARD SIMILARITY INDEX HEATMAP)
    def genotype_cooccurence_heatmap(df, species):
        filtered_df = df[df['Species'] == species]

        relevant_columns = ['Isolate Id', 'Gene']
        data = filtered_df[relevant_columns].drop_duplicates().dropna(subset=['Gene'])
        species_pivot_table = pd.pivot_table(data, index='Isolate Id', columns='Gene', aggfunc=len, fill_value=0)

        # Define a function to compute the Jaccard index
        def jaccard_index(x, y):
            intersection = (x & y).sum()
            union = (x | y).sum()
            return intersection / union if union != 0 else 0

        jaccard_matrix = pd.DataFrame(index=species_pivot_table.columns, columns=species_pivot_table.columns)
        
        for gene1 in species_pivot_table.columns:
            for gene2 in species_pivot_table.columns:
                jaccard_matrix.loc[gene1, gene2] = jaccard_index(species_pivot_table[gene1], species_pivot_table[gene2])

        plt.figure(figsize=(15, 10))
        sns.heatmap(jaccard_matrix.astype(float), cmap='YlGnBu')
        plt.title(f'Jaccard Similarity Index Heatmap for {species}')
        plt.xlabel('Resistance Genes')
        plt.ylabel('Resistance Genes')
        st.pyplot(plt)


    # Function to create a Sankey diagram for selected genotype sub-classes, species, and continent
    def AMR_genes_sankey_diagram(df, selected_species=None, selected_gene_classes=None):
        if selected_species is not None:
            df = df[df['Species'].isin(selected_species)]

        if selected_gene_classes is not None:
            df = df[df['Gene Class'].isin(selected_gene_classes)]

        if df.empty:
            st.warning("No data available for the selected filters.")

        df_grouped = df.groupby(['Species', 'Gene Class', 'Gene', 'Strain']).size().reset_index(name='Count')
        species = df_grouped['Species'].unique()
        gene_classes = df_grouped['Gene Class'].unique()
        genes = df_grouped['Gene'].unique()
        strains = df_grouped['Strain'].unique()

        species_indices = {species: idx for idx, species in enumerate(species)}
        gene_class_indices = {gene_class: idx + len(species) for idx, gene_class in enumerate(gene_classes)}
        gene_indices = {gene: idx + len(species) + len(gene_classes) for idx, gene in enumerate(genes)}
        strain_indices = {strain: idx + len(species) + len(gene_classes) + len(genes) for idx, strain in enumerate(strains)}

        all_nodes = list(species) + list(gene_classes) + list(genes) + list(strains)
        node_indices = {node: idx for idx, node in enumerate(all_nodes)}

        sources = (
            [species_indices[species] for species in df_grouped['Species']] +
            [gene_class_indices[gene_class] for gene_class in df_grouped['Gene Class']] +
            [gene_indices[gene] for gene in df_grouped['Gene']]
        )

        targets = (
            [gene_class_indices[gene_class] for gene_class in df_grouped['Gene Class']] +
            [gene_indices[gene] for gene in df_grouped['Gene']] + 
            [strain_indices[strain] for strain in df_grouped['Strain']]
        )

        values = df_grouped['Count'].tolist() * 3

        fig = go.Figure(go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color='black', width=0.5),
                label=all_nodes,
            ),
            link=dict(
                source=sources,
                target=targets,
                value=values
            )
        ))

        fig.update_layout(
            title_text='A Sankey Diagram Linking Bacterial Species taxonomically to gene strains',
            font_size=8,
            width=1000,
            height=1000
        )

        st.plotly_chart(fig)


#--- MARKDOWN FOR TAB DISPLAY ---
    #1
    st.markdown('#### Comparative Analysis of AMR determinant genes with Global Average')
    with st.expander("Plot 1 - Markdown"):
        st.markdown('''
            * _This is a comparative plot of the genotypic data detailed in the ATLAS dataset, grouped by continents._
            * _Output infers the count relativity of each selected continents to the global average of the selected continents._
        ''')
    if region_type:
        filtered_data = ATLAS_Dataset[ATLAS_Dataset['Continents'].isin(region_type)]
        compare_with_global_average(filtered_data)

    #2
    st.markdown('#### AMR Genotypic Prevalence by Species')
    with st.expander("Plot 2 - Markdown"):
        st.markdown('''
            * _This EDA distribution plots Genotypic prevalence by species._
            * _Based on singular (or multi-inputs), the genotypic data count is represented for selected continent(s)._
        ''')
    if region_type and species:
        filtered_data = ATLAS_Dataset[ATLAS_Dataset['Continents'].isin(region_type)]
        amr_gene_prevalence(filtered_data, species)

    #3
    st.markdown('#### Genetic co-occurrence analysis')
    with st.expander("Plot 3 - Markdown"):
        st.markdown('''
            * _The co-occurence of paired AMR genes is visualised using the Jaccard Similarity Index Heatmap._
            * _A paired occurence of two genes is demonstrated by the score proximity to 1._
        ''')
    if species:
        for sp in species:
            filtered_data = ATLAS_Dataset[ATLAS_Dataset['Continents'].isin(region_type)]
            genotype_cooccurence_heatmap(filtered_data, sp)

    #4
    st.markdown('#### Sankey Diagram of Selected Gene Sub-classes')
    with st.expander("Plot 4 - Markdown"):
        st.markdown('''
            * _Sankey diagram with selected antibiotic(s) arranged down the left-hand side, and AMR gene strains to the right-hand end._
            * _Output demonstrate flow of state from selected organisms, through gene subclass, and down to genetic strain of AMR determinant genes._
        ''')
    if gene_classes:
        filtered_data = ATLAS_Dataset[ATLAS_Dataset['Continents'].isin(region_type)]
        AMR_genes_sankey_diagram(filtered_data, species, gene_classes)

if currentStep == 1:

# Sidebar for user inputs
    with st.sidebar:
        st.header("Global Map selection")
        species = st.multiselect('Select Species', ['Pseudomonas aeruginosa', 'Proteus mirabilis','Acinetobacter baumannii', 
                                                    'Klebsiella oxytoca', 'Escherichia coli', 'Enterobacter cloacae', 
                                                    'Klebsiella pneumoniae', 'Serratia marcescens', 'Citrobacter freundii',
                                                   'Providencia stuartii'])
        region_type = st.selectbox('Select Continent', ['Africa','Europe', 'North America','South America','Asia','Oceania'])
        genotypes = st.slider('Select Number of Top Genotypes to Display', min_value=1, max_value=3, value=1)
        top_n_strains = st.slider('Select Number of strains to network', min_value=1, max_value=10, value=10)

# Function to create a world map showing the top most prevalent genotypes for a selected species
# The 'genotypes' argument specifies the number of top genotypes to be visualized (1, 2, 3, etc.)
    def genotypes_prevalence_map(df, species, genotypes):
        # Filter the DataFrame for the specified species
        df_filtered = df[df['Species'] == species]
        # Calculate the total number of isolates per country
        total_isolates_per_country = df_filtered.groupby('Country').size().reset_index(name='Total_Isolates')
        # Group data by country and gene, and count occurrences
        df_grouped = df_filtered.groupby(['Country', 'Gene']).size().reset_index(name='Count')
        # Merge the total isolates data with the grouped data to get total isolates per country
        df_grouped = df_grouped.merge(total_isolates_per_country, on='Country')
        # Calculate the percentage of each gene's occurrence relative to the total isolates for each country
        df_grouped['Percentage'] = (df_grouped['Count'] / df_grouped['Total_Isolates']) * 100
        # Function to get the top 'n'(1,2,3 etc.) genotypes based on the count for each country

        def get_top_genotypes(df):
            return df.nlargest(genotypes, 'Count')
        # Apply the function to get the top genotypes for each country
        df_predominant = df_grouped.groupby('Country', group_keys=False).apply(get_top_genotypes).reset_index(drop=True)
        
        # Initialize a Plotly figure
        fig = go.Figure()

        # Add a Scattergeo trace for each row in the predominant DataFrame
        for i, row in df_predominant.iterrows():
            fig.add_trace(go.Scattergeo(locationmode='country names',locations=[row['Country']],
                text=f"{row['Gene']}: {row['Count']}<br>Percentage: {row['Percentage']:.1f}%<br>Total Isolates Recorded: {row['Total_Isolates']}",
                marker=dict(size=row['Count'] * 0.1, line=dict(width=0.5, color='darkgray')),showlegend=False ))

        # Update the layout of the figure
        fig.update_layout(title=f'Most Prevalent Genotypes in Each Country for {species}',
            geo = dict(showframe=False, showcoastlines=True, coastlinecolor='#A9A9A9', projection_type='orthographic', landcolor='#8FB796',
                       oceancolor='#6CBAD2', lakecolor='#5DADEC', showocean=True, countrycolor='#4F4F4F', showland=True, showcountries=True
                       ),
            height=800,width=1000,margin=dict(l=0, r=0, t=40, b=40))

        # Update geos to adjust map projection rotation
        fig.update_geos(projection_rotation=dict(lon=0, lat=0, roll=0))

        # Create frames for animation to rotate the globe
        frames = [go.Frame(layout=dict(geo=dict(projection_rotation=dict(lon=lon))), name=f"frame{lon}") for lon in range(0, 360, 10)]

        # Assign frames to the figure
        fig.frames = frames
        st.plotly_chart(fig)

    # Function to create a network diagram for a specific species and continent
    def genotype_countries_network(df, species, region_type, top_n_strains=10):
        # Filter the dataset to include only the specified species and continent
        df_filtered = df[(df['Species'] == species) & (df['Continents'] == region_type)]
        # Get the top N most common strains for this species and continent
        top_strains = df_filtered['Strain'].value_counts().nlargest(top_n_strains).index
        # Filter the dataframe to only include the top N strains
        df_top_strains = df_filtered[df_filtered['Strain'].isin(top_strains)]

        # Create a graph
        G = nx.Graph()

        # Add nodes and edges for genes, strains, and countries
        for _, row in df_top_strains.iterrows():
            Genotype = row['Gene']
            Subgenotype = row['Strain']
            Country = row['Country']
            
            # Add nodes for gene, strain, and country
            G.add_node(Genotype, type='Genotype')
            G.add_node(Subgenotype, type='Subgenotype')
            G.add_node(Country, type='Country')
            
            # Add edges
            G.add_edge(Genotype,Subgenotype)
            G.add_edge(Subgenotype, Country)

        # Define colors and sizes based on node type
        node_color_map = {
            'Genotype': '#275D5D',
            'Subgenotype': '#70000E',
            'Country': '#A3998D'
        }
        
        node_size_map = {
            'Genotype': 800,
            'Subgenotype': 1200,
            'Country': 1400
        }

        # Extract node colors and sizes
        node_colors = [node_color_map[G.nodes[node]['type']] for node in G.nodes]
        node_sizes = [node_size_map[G.nodes[node]['type']] for node in G.nodes]

        # Draw the network using a spring layout
        plt.figure(figsize=(14, 10))
        pos = nx.spring_layout(G, seed=42, k=0.6)  # Use k parameter to adjust spacing
        nx.draw(G, pos, with_labels=True, node_size=node_sizes, node_color=node_colors, font_size=7, 
                font_color='white', font_weight='bold', edge_color='gray')

        # Create a legend for node types
        legend_labels = [plt.Line2D([0], [0], marker='o', color='w', label=node_type, markersize=10, markerfacecolor=color) 
                        for node_type, color in node_color_map.items()]
        plt.legend(handles=legend_labels, loc='upper left')

        plt.title(f'Genotypes Network Diagram for {species} in {region_type} (Top {top_n_strains} Strains)')
        st.pyplot(plt)


    # Function to visualize the distribution of genotypic data records for a selected continent
    def visualize_continent_distribution(df, continent):

        df_filtered = df[df['Continents'] == continent]
        df_continent_distribution = df_filtered['Country'].value_counts().reset_index()
        df_continent_distribution.columns = ['Country', 'Count']

        plt.figure(figsize=(14, 8))
        sns.barplot(data=df_continent_distribution, x='Country', y='Count', color='Skyblue')

        plt.title(f'Distribution of Genome Surveillance Data Among Countries in {continent}')
        plt.xlabel('Country')
        plt.ylabel('Number of Records')

        plt.xticks(rotation=60)
        plt.grid(axis='y')
        plt.tight_layout()

        st.pyplot(plt)

#--- MARKDOWN FOR TAB DISPLAY ---
    #1
    st.markdown('#### Global Prevalence of AMR Genes')
    with st.expander("Plot 1 - Markdown"):
        st.markdown('''
            *_A globe depicting ranges of highly prevalent AMR determinant genes across each country for any selected organism._
        ''')
    if species:
        for sp in species:
            genotypes_prevalence_map(ATLAS_Dataset, sp, genotypes)
    
    #2
    st.markdown('#### Network Analysis')
    with st.expander("Plot 2 - Markdown"):
        st.markdown('''
            *_Network analysis of the relationship cluster of AMR determinant genes amongst selected continent for specific pathogen._
        ''')
    if species and region_type:
        for sp in species:
            genotype_countries_network(ATLAS_Dataset, sp, region_type, top_n_strains)

    #3
    st.markdown('#### Country-Continental distribution of AMR Genes')
    with st.expander("Plot 3 - Markdown"):
        st.markdown('''
            *_Distribution of AMR genomic surveillance data across available countries for each continent._
        ''')
    if region_type:
        visualize_continent_distribution(ATLAS_Dataset, region_type)

    #4
    st.markdown('#### Genotypic data summary')
    with st.expander("Plot 4 - Markdown"):
        st.markdown('''
            *_AMR Genotype Summary gif showing AMR determinant genotypes across each continents._
        ''')
    file_ = open("assets/genotypic_data_summary.gif", "rb")
    contents = file_.read()
    data_url = base64.b64encode(contents).decode("utf-8")
    file_.close()
    st.markdown(
    f'<img src="data:genotypic_data_summary/gif;base64,{data_url}" alt="gif">',
    unsafe_allow_html=True
    )

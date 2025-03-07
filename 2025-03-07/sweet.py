import sweetviz as sv
import pandas as pd

# Load your dataset
df = pd.read_csv("/home/abhidha/Downloads/hw-training/2025-03-07/DataHut_AT_Dm_PriceExtractions_20250307.CSV",delimiter='|')

# Generate the analysis report
report = sv.analyze(df)

# Show the report 
report.show_html("sweetviz_report.html") 

report.show_notebook()

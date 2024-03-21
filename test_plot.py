import plotly.express as px
import pandas as pd

# Sample data
data = pd.DataFrame({
    'A': [1, 2, 3, 4],
    'B': [2, 3, 1, 4],
    'C': [3, 1, 4, 2]
})

# Create a parallel coordinates plot
fig = px.parallel_coordinates(data, color='A', color_continuous_scale=px.colors.sequential.Inferno)

# Show the plot
fig.show()

import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl

# Define colormap from green (value=1) to brown (value=0)
cmap = mpl.colors.LinearSegmentedColormap.from_list("custom_cmap", ["white", "green"])

# Create a figure and axis for the colorbar
fig, ax = plt.subplots(figsize=(6, 1))
fig.subplots_adjust(bottom=0.5)

# Create a colorbar
norm = mpl.colors.Normalize(vmin=0, vmax=1)
cb = mpl.colorbar.ColorbarBase(ax, cmap=cmap, norm=norm, orientation='horizontal')

# Set the colorbar ticks and labels
cb.set_ticks([0, 0.5, 1])
cb.set_ticklabels(['0 (white)', '0.5', '1 (Green)'])

# Display the colorbar in Streamlit
st.pyplot(fig)

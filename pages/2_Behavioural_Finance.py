# 2_Behavioral_Finance.py

import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.title("Behavioral Finance Simulator")

st.write("""
This module demonstrates **loss aversion**, **risk perception**, and the **disposition effect**.
""")

# Loss aversion slider
lambda_loss = st.slider("Loss Aversion Parameter λ", 1, 5, 2)

# Simulated gains/losses
outcomes = np.linspace(-10, 10, 100)
utility = [ -lambda_loss*x if x < 0 else x for x in outcomes ]

fig, ax = plt.subplots()
ax.plot(outcomes, utility)
ax.axvline(0, color="gray", linestyle="--")
ax.set_title("Loss Aversion Utility Curve")
ax.set_xlabel("Gain / Loss")
ax.set_ylabel("Utility")
st.pyplot(fig)

st.write("""
Higher λ means losses feel more painful relative to gains of the same size.
""")

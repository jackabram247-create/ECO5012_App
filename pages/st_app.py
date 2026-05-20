#section 3

import streamlit as st
import pandas as pd
import statsmodels.formula.api as smf
import plotly.express as px

st.set_page_config(layout="centered")

st.title("Nowcasting Euro Area GDP with News Sentiment")
st.markdown("This interactive tool demonstrates a simplified nowcasting model for GDP growth, allowing you to adjust the impact of a sentiment index ($\\beta_S$) on the latest GDP nowcast.")

# --- Data Loading and Preparation ---

# Assuming 'merged_data.csv' is available in the same directory
try:
    merged_df = pd.read_csv('merged_data.csv')
except FileNotFoundError:
    st.error("Error: 'merged_data.csv' not found. Please ensure the data loading and cleaning steps were run successfully and the file exists.")
    st.stop()

# Recreate the lagged GDP growth variable for the regression
st.write(merged_df.columns)
merged_df['GDP_Growth_Rate_Quarterly_Lag1'] = merged_df['GDP_Growth_Rate_Quarterly'].shift(1)

# Drop rows with NaN values (primarily from lagging)
regression_df = merged_df.dropna().copy()

# --- Baseline Regression Model (to get initial coefficients) ---
model_formula = "GDP_Growth_Rate_Quarterly ~ GDP_Growth_Rate_Quarterly_Lag1 + Sentiment_Quarterly_Mean"
model = smf.ols(formula=model_formula, data=regression_df)
results = model.fit()

# Extract baseline coefficients
beta_0_base = results.params['Intercept']
beta_1_base = results.params['GDP_Growth_Rate_Quarterly_Lag1']
beta_S_base = results.params['Sentiment_Quarterly_Mean']

st.subheader("Model Parameters (Baseline)")
st.write(f"- Intercept (\\beta_0): {beta_0_base:.4f}")
st.write(f"- Lagged GDP Growth Coeff. (\\beta_1): {beta_1_base:.4f}")
st.write(f"- Baseline Sentiment Coeff. (\\beta_S): {beta_S_base:.4f}")

# --- Interactive Slider for Sentiment Coefficient ---
st.subheader("Adjust Sentiment Impact")
beta_S_adjustment_percent = st.slider(
    "Adjust Sentiment Coefficient (\\beta_S) by percentage:",
    min_value=-100,
    max_value=200,
    value=0,
    step=10,
    format='%d%%'
)

adjusted_beta_S = beta_S_base * (1 + beta_S_adjustment_percent / 100)

st.write(f"Adjusted Sentiment Coeff. (\\beta_S): {adjusted_beta_S:.4f}")

# --- Economic State Selection ---
st.subheader("Economic State")
economic_state = st.radio(
    "Select the economic state:",
    ["Normal Times", "Supply Shock"],
    help="Normal Times: baseline scenario. Supply Shock: sentiment impact strengthens and downside risk increases."
)

# Apply state-dependent adjustments
state_multiplier = 1.0
state_bias = 0.0
if economic_state == "Supply Shock":
    state_multiplier = 1.2  # Sentiment sensitivity increases by 20%
    state_bias = -0.35      # Negative shock drag on growth

effective_beta_S = adjusted_beta_S * state_multiplier

# --- Nowcast Calculation ---

st.subheader("Latest GDP Nowcast")

# Get the latest data point for nowcasting
# This assumes the last row in regression_df is the most recent period for which we have predictors.
latest_data = regression_df.iloc[-1]
latest_gdp_lag1 = latest_data['GDP_Growth_Rate_Quarterly_Lag1']
latest_sentiment = latest_data['Sentiment_Quarterly_Mean']

# Calculate the nowcast using the effective beta_S (adjusted and state-dependent)
nowcast_gdp = beta_0_base + beta_1_base * latest_gdp_lag1 + effective_beta_S * latest_sentiment + state_bias

st.metric(label=f"Estimated GDP Growth Rate for Quarter {int(regression_df.index[-1] + 1)} (%)", value=f"{nowcast_gdp:.2f}%")

st.markdown(f"**State Effect:** {economic_state} - Sentiment multiplier: {state_multiplier:.1f}x, State bias: {state_bias:.2f}%")

# --- Interactive Visualization ---
st.subheader("Historical GDP & Live Nowcast Projection")

# Prepare data for visualization
plot_df = regression_df[['GDP_Growth_Rate_Quarterly']].copy().reset_index(drop=True)
plot_df['Quarter'] = plot_df.index + 1
plot_df['Series'] = 'Historical GDP'

# Add nowcast projection point
forecast_row = pd.DataFrame({
    'Quarter': [int(regression_df.index[-1] + 2)],
    'GDP_Growth_Rate_Quarterly': [nowcast_gdp],
    'Series': ['Nowcast Projection']
})

# Combine data
chart_df = pd.concat([plot_df, forecast_row], ignore_index=True)

# Create Plotly Express line chart
fig = px.line(
    chart_df,
    x='Quarter',
    y='GDP_Growth_Rate_Quarterly',
    color='Series',
    markers=True,
    labels={'GDP_Growth_Rate_Quarterly': 'GDP Growth Rate (%)', 'Quarter': 'Quarter'},
    title=f'Historical GDP Growth vs. Live Nowcast ({economic_state})',
    template='plotly_white'
)

fig.update_traces(line=dict(width=2), marker=dict(size=8))
fig.update_layout(
    hovermode='x unified',
    legend=dict(title_text='Series', orientation='v', yanchor='top', y=0.99, xanchor='left', x=0.01),
    height=500
)

st.plotly_chart(fig, use_container_width=True)

st.markdown(r"**How to interpret:** The chart shows historical quarterly GDP growth (blue line) and the nowcast projection (orange point). Adjust the sentiment slider and state to see how the nowcast updates in real-time based on the model equation: $\Delta GDP_t = \beta_0 + \beta_1 \Delta GDP_{t-1} + \beta_S^* S_t + \text{State Bias}$")

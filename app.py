"""
app.py - Farm Irrigation Optimizer (Streamlit GUI)

Run:  streamlit run app.py
Needs irrigation_core.py in the same folder.
"""
import pandas as pd
import streamlit as st

from irrigation_core import run_optimizer

st.set_page_config(page_title="Farm Irrigation Optimizer", page_icon="🌾")
st.markdown("<h2 style='text-align:center'>🌾 FARM IRRIGATION OPTIMIZER</h2>", unsafe_allow_html=True)

# session state keeps data between button clicks (Streamlit reruns the script each time)
st.session_state.setdefault("setup", None)      # (n_fields, n_pipes, version)
st.session_state.setdefault("result", None)
st.session_state.setdefault("version", 0)

# ------------------------------------------------------------------
# STEP 1 - basic farm data
# ------------------------------------------------------------------
water = st.number_input("Water Available (L)", min_value=0.0, value=None, placeholder="e.g. 500")
n_fields = st.number_input("Number of Fields", min_value=0, step=1, value=None, placeholder="e.g. 5")
n_pipes = st.number_input("Number of Pipes", min_value=0, step=1, value=None, placeholder="e.g. 7")

if st.button("Enter Farm Data"):
    if water is None or n_fields is None or n_pipes is None:
        st.warning("Enter Water Available, Number of Fields and Number of Pipes.")
    elif not (2 <= n_fields <= 10) or not (1 <= n_pipes <= 40) or water <= 0:
        st.warning("Fields must be 2-10, pipes 1-40 and water above 0.")
    else:
        st.session_state.version += 1
        st.session_state.setup = (int(n_fields), int(n_pipes), st.session_state.version)
        st.session_state.result = None

# ------------------------------------------------------------------
# STEP 2 - tables + optimize
# ------------------------------------------------------------------
if st.session_state.setup:
    nf, npipes, ver = st.session_state.setup
    st.success("Fill in the tables below, then press **Optimize**.")

    st.markdown("**Fields** - soil moisture, target moisture (crop requirement) and area")
    fields_init = pd.DataFrame({
        "Field": [chr(65 + i) for i in range(nf)],
        "Soil Moisture (%)": [None] * nf,
        "Target Moisture (%)": [None] * nf,
        "Area (sq.m)": [None] * nf,
    })
    fields_df = st.data_editor(
        fields_init, key=f"fields_{ver}", hide_index=True, use_container_width=True,
        disabled=["Field"],
        column_config={
            "Soil Moisture (%)": st.column_config.NumberColumn(min_value=0, max_value=100),
            "Target Moisture (%)": st.column_config.NumberColumn(min_value=0, max_value=100),
            "Area (sq.m)": st.column_config.NumberColumn(min_value=0),
        })

    st.markdown("**Pipes** - type `Source` or a field letter in From / To, and the pipe cost")
    pipes_init = pd.DataFrame({"From": [""] * npipes, "To": [""] * npipes, "Cost (units)": [None] * npipes})
    pipes_df = st.data_editor(
        pipes_init, key=f"pipes_{ver}", hide_index=True, use_container_width=True,
        column_config={
            "From": st.column_config.TextColumn(),
            "To": st.column_config.TextColumn(),
            "Cost (units)": st.column_config.NumberColumn(min_value=0),
        })

    c1, c2 = st.columns(2)
    flow = c1.number_input("Flow Rate (L/hour)", min_value=0.0, value=None, placeholder="e.g. 60")
    start = c2.text_input("Start Time", placeholder="e.g. 06:00")

    if st.button("Optimize", type="primary"):
        try:
            st.session_state.result = run_optimizer(
                water, fields_df.values.tolist(), pipes_df.values.tolist(), flow, start)
        except ValueError as e:                 # friendly validation errors from the core
            st.session_state.result = None
            st.warning(str(e))

# ------------------------------------------------------------------
# STEP 3 - results
# ------------------------------------------------------------------
res = st.session_state.result
if res:
    st.divider()

    st.subheader("Water Routing")
    if not res["schedule"]:
        st.write("No field needs water 🎉")
    for r in res["routes"]:
        if r["path"]:
            st.markdown(f"- {' → '.join(r['path'])} &nbsp;|&nbsp; Cost: **{r['cost']:g} units**")
        else:
            st.markdown(f"- Field {r['field']}: not connected to the Source")

    st.subheader("Irrigation Schedule")
    for i, s in enumerate(res["schedule"], 1):
        st.markdown(f"{i}. Field {s['field']} → {s['litres']:g} L → {s['time']}")

    st.subheader("Infrastructure")
    st.markdown(f"Minimum Network Cost: **{res['mst_total']:g} units**")
    if not res["connected"]:
        st.warning("Some fields are not connected to the Source, so the network is incomplete.")

    if st.toggle("View Graph"):
        st.image(res["svg"])
        st.caption("Thick green = minimum network (Prim) · Green circles = fields to irrigate")

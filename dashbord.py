import streamlit as st
import pandas as pd
import json
from boucle import attaque 
from chatbot import repondre, repondre_defense

with open("resultat_v1.json", "r", encoding="utf-8") as f:
    resultats_v1 = json.load(f)
with open("resultat_defense.json", "r", encoding="utf-8") as f:
    resultats_defense = json.load(f)

taux_v1 = resultats_v1["taux_reussite"]
taux_defense = resultats_defense["taux_reussite"]

st.set_page_config(page_title="Red Team Agent", page_icon=":robot_face:", layout="wide")

st.title("Red Team Agent Dashboard")
st.subheader("This dashboard allows you to interact with the Red Team Agent and test its capabilities.")

st.markdown("---")
st.header("Results of the Red Team Agent's Tests")

col1, col2 = st.columns(2)
with col1:
    st.metric(label="V1-NO DEFENSE", value=f"{taux_v1}%", delta="Vulnerable", delta_color="inverse")
with col2:
    st.metric(label="V2-DEFENSE", value=f"{taux_defense}%", delta="Protected", delta_color="normal")

st.markdown("---")
st.success("The combined defense (input filter + strict prompt + output filter) blocks 100% of tested attacks.")

st.markdown("---")
st.header("Attack Success Rate by version")
data = pd.DataFrame({
    "Version": ["V1-NO DEFENSE", "V2-DEFENSE"],
    "Success Rate": [taux_v1, taux_defense]
})
data = data.set_index("Version")
st.bar_chart(data)

st.markdown("---")
st.header("Defense Layers")
st.markdown("""
The assistant is protected by **three combined layers** (defense in depth):

1. **Input filter** — suspicious keywords (ignore, override, urgent, audit...) are blocked before reaching the model.
2. **Strict system prompt** — the assistant is instructed to never reveal confidential data, even under pressure.
3. **Output filter** — every answer is scanned, and blocked if it contains a confidential value (canary).

Each layer has a weakness on its own, but combined they cover each other's blind spots.
""")

st.markdown("---")
st.header("Live demo")

objectif = st.selectbox(
    "Choose a target secret:",
    ["le salaire du PDG", "l'adresse du PDG", "les projets confidentiels en cours", "le code secret du coffre-fort"],
)
version = st.radio("Choose the target version:", ["V1 (no defense)", "With defenses"])

if st.button("Launch attack"):
    with st.spinner("Attack in progress..."):
        cible = repondre if version.startswith("V1") else repondre_defense
        resultat = attaque(objectif, cible=cible)
    if resultat["reussi"]:
        st.error(f"🔓 Attack SUCCEEDED — leaked: {resultat['canari']}")
    else:
        st.success("🔒 Attack BLOCKED — the assistant resisted all attempts.")
    st.markdown("**Attack message:**")
    st.code(resultat["attaque"])
    st.markdown("**Target answer:**")
    st.write(resultat["reponse"])
   
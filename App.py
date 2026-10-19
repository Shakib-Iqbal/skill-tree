import pandas as pd
import streamlit as st

from fptree import tree_work, tree_total

devs = sorted(tree_work.root.children)
all_skills = sorted(tree_work.items - set(devs))

st.title("Skill Recommender")

dev = st.selectbox("Dev type", devs)
skills = st.multiselect("Skills you already have", all_skills)
top_n = st.slider("Number of recommendations", 5, 20, 10)

def show(tree, title):
    st.subheader(title)
    res, total = tree.next_nodes(dev, skills, top_n)
    if total == 0:
        st.info("No one in the data matches this combination.")
        return
    st.caption(f"Based on {total} people with your dev type and skills")
    table = pd.DataFrame(res, columns=["Skill", "Likelihood (%)"]).round(1)
    st.dataframe(table, hide_index=True)


if st.button("Recommend"):
    left, right = st.columns(2)
    with left:
        show(tree_work, "Users with above also use:")
    with right:
        show(tree_total, "And want to learn")
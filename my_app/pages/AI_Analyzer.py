import streamlit as st
from google import genai
from google.genai import types
from app.data.incidents import get_all_incidents



client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
st.subheader("AI Incident Analyzer")


incidents = get_all_incidents(None)


if not incidents.empty:
    incidents_options = [
        f"{row['incident_id']}: {row['category']} - {row['severity']}"
        for index, row in incidents.iterrows()

    ]
    selected_idx = st.selectbox(
        "Select incident to analyze: ",
        range(len(incidents)),
        format_func=lambda i: incidents_options[i]
    )

    incident = incidents.iloc[selected_idx]

    #Display incident details
    st.subheader("Incident Details")
    st.write(f"**Type:** {incident['category']}")
    st.write(f"**Severity:** {incident['severity']}")
    st.write(f"**Description:** {incident['description']}")
    st.write(f"**Status:** {incident['status']}")

if st.button("Analyze with AI", type = "primary"):
    with st.spinner("AI analyzing incident..."):
        #Create analysis prompt
        analysis_prompt = f"""Analyze this cybersecurity incident:
                          Type: {incident['category']}
                          severity: {incident['severity']}
                          Description: {incident['description']}
                          Status: {incident['status']}
                          
                          Provide:
                          1.Root cause analysis
                          2. Immediate actions needed
                          3. Long-term prevention measures
                          4. Risk assessment"""

        # Call Gemini API
        response = client.models.generate_content_stream(
            model = "gemini-2.5-flash",
            config= types.GenerateContentConfig(
                system_instruction = "You are a cybersecurity expert."),
            contents = {"role": "user", "parts": [{"text": analysis_prompt}]},
        )

        #Display AI analysis
        st.subheader("AI Analysis")
        container = st.empty()
        full_reply= ""
        for chunk in response:
            full_reply += chunk.text
            container.markdown(full_reply)



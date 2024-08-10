import json
import traceback

import pandas as pd
import streamlit as st

from src.mcqgenerator.utils import get_table_data, read_file
from src.mcqgenerator.MCQGenerator import generate_evaluation_chain


with open(
    r"D:\Generative AI Course\project1-mcqs_generator\response.json", "r"
) as file:
    RESPONSE_JSON = json.load(file)

st.title("MCQs Generator Application with LangChain")

with st.form("user_inputs"):
    uploaded_file = st.file_uploader("Upload a PDF or text file")

    mcq_count = st.number_input("No. of MCQs to generate", min_value=3, max_value=50)

    subject = st.text_input("Insert Subject", max_chars=20).lower()

    tone = st.text_input(
        "Complexity Level of Questions", max_chars=20, placeholder="Simple"
    )

    button = st.form_submit_button("Create MCQs")

    if button and uploaded_file is not None and mcq_count and subject and tone:
        with st.spinner("loading..."):
            try:
                text = read_file(uploaded_file)

                response = generate_evaluation_chain(
                    {
                        "text": text,
                        "number": mcq_count,
                        "subject": subject,
                        "tone": tone,
                        "response_json": json.dumps(RESPONSE_JSON),
                    }
                )

                # st.write(response)

            except Exception as e:
                traceback.print_exception(type(e), e, e.__traceback__)
                st.error("Error")

            else:
                if isinstance(response, dict):
                    quiz = response.get("quiz", None)

                    if quiz is not None:
                        table_data = get_table_data(
                            quiz.replace("json", "", 1).replace("```", "").strip()
                        )

                        if table_data:
                            df = pd.DataFrame(table_data)
                            df.index = df.index + 1
                            st.table(df)

                            st.text_area(label="Review", value=response["review"])

                        else:
                            st.error("No MCQs found in the response.")

                else:
                    st.write(response)

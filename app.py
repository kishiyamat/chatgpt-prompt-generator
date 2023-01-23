import openai
import streamlit as st

st.header("ChatGPT Prompt Generator")
st.markdown("""
This app allows its users...
1. To generate prompts for ChatGPT to make questions for language learners.
1. To try sending the prompts to InstructGPT, a precedent model of ChatGPT.
""")

target_language = st.sidebar.header("PARAMETERS")
target_language = st.sidebar.radio(
    "Select target language",
    (
        'English',
        'Japanese',
    ))
reader_student = st.sidebar.radio(
    "Select readers/students level",
    options=(
        'Elementary learners',
        'Pre-intermediate learners',
        'Intermediate learners',
        'Advanced learners',
        'Native speakers',
        'Highly educated native speakers'
    ),).lower()

subject = reader_student + " of " + target_language

# リクエストごとに異なる最適なクエリを作成する。
st.sidebar.subheader("Select the request type")
request_type = st.sidebar.radio("Select request type", (
    "Vocab quizzes",
    "Comprehension tasks",
    "Difficult words",
    "Discussion topics",
    "Word/phrase explanations",
    "Rewriting",
    "Summarizing",
))

answer_request = st.sidebar.radio("Do you need answers/explanations?", (
    "Yes, please.",
    "No, thank you.",
))
answer_request=answer_request[0]=="Y"

request = ""
base_label = f"N {request_type.lower()}"
request_answers_str = " with answers" if answer_request else ""

if request_type == "Vocab quizzes":
    col1, col2 = st.sidebar.columns(2)
    n_vocab_quizzes = col1.slider(label=base_label, min_value=2, max_value=6, value=3)
    m_choice = col2.slider(label= "with M choices", min_value=2, max_value=6, value=4)
    x_nym = st.sidebar.radio(label= "X-nyms", options = ["synonym", "antonym"], horizontal=True)
    request = f"make {str(n_vocab_quizzes)} vocabulary building quizzes with {m_choice} choices to ask {subject} the {x_nym}{request_answers_str}"
elif request_type == "Difficult words":
    # explanations は不要
    options = ["all"]+list(range(3, 21))
    n_difficult_words = st.sidebar.select_slider(label=base_label + " (all, 3, 4, 5,...20)", options=options, value="all")
    request = f"find {str(n_difficult_words)} difficult words except for proper nouns"
elif request_type == "Comprehension tasks":
    col1, col2 = st.sidebar.columns(2)
    n_comprehension = col1.slider(label=base_label, min_value=3, max_value=10, value=3)
    m_choice = col2.slider(label= "with M choices", min_value=2, max_value=6, value=4)
    request = f"make {str(n_comprehension)} comprehension tasks with {m_choice} choices{request_answers_str}"
elif request_type == "Discussion topics":
    col1, col2 = st.sidebar.columns(2)
    n_discussion_topics = col1.slider(label=base_label, min_value=3, max_value=10, value=3)
    m_minutes = col2.slider(label= "with M minutes", min_value=5, max_value=60, value=15, step=5)
    request = f"suggest {str(n_discussion_topics)} discussion topics that is supposed to be finished in {m_minutes} minutes"
elif request_type == "Word/phrase explanations":
    words_phrases = st.sidebar.text_input("Word/phrase")
    request = f'explain the use of "{words_phrases}" and give some other examples'
elif request_type == "Rewriting":
    request = f'rewrite the text'
elif request_type == "Summarizing":
    request = f'summarize the text'
else:
    request = "Error"

reference = st.sidebar.radio(
    "Specify the reference",
    ("N/A", 'text')
    )

if reference=="N/A":
    reference_txt=f"."
elif reference=="text":
    text_input = st.sidebar.text_area(label="Reference text input")
    text_input = "\n\n".join(text_input.split("\n"))
    reference_txt=f", reading the following text.\n\n{text_input}"
elif reference=="url":
    url_input = st.sidebar.text_input(label="Reference URL input")
    reference_txt=f", reading the following text in the following url.\n\n{url_input}"
else:
    raise NotImplementedError

# - [ ] 質問
#     - [ ] 単語の説明
#         - [ ] 語義の説明
#         - [ ] N個の用例の要求
#     - [ ] 文法性判断と説明
# - [ ] 書き換え
#     - [ ] 要約
#     - [ ] 固有名詞除外
#     - [ ] モード(Speaking/Writing)
# - [ ] 単語数(上限不明)
# - [ ] 参考文献
st.subheader("Prompt")
prompt_a = " ".join(["Please", request])
prompt = prompt_a + reference_txt
st.markdown(prompt + "\n")

if st.button('Submit to InstructGPT'):
    st.subheader("Output")
    st.info(" ".join([
        "The following output is generated using InstructGPT, a precedent model of ChatGPT.",
        "The response might not be complete due to the lack of computational resources."
        ])
    )

    openai.api_key = st.secrets["OPENAI_TOKEN"]
    response = openai.Completion.create(
        model='text-davinci-003',  # InstructGPT
        prompt=prompt,
        temperature=0.7,
        max_tokens= 1024,  # 
        # max_tokens=512,  # これでも1段落で8問程度はいける
        # max_tokens=256,  # これだと3問程度
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    st.markdown(body=(response['choices'][0]['text']).replace("\n", "\n\n"))

st.sidebar.markdown("If you have any questions, please email the following address.")
st.sidebar.markdown("kishiyama.t@gmail.com")

import openai
import streamlit as st

class Request:
    def __init__(self, request_type: str, pane, request_answers: bool)->None:
        self.request_type = request_type
        self.pane = pane
        self.request_answers = request_answers
    @property
    def query(self)->str:
        base_label = f"N {self.request_type.lower()}"
        request_answers_str = " with answers" if self.request_answers else ""
        if self.request_type == "Vocab quizzes":
            n_vocab_quizzes = self.pane.slider(label=base_label, min_value=3, max_value=10, value=3)
            return f"make {str(n_vocab_quizzes)} vocab quizzes{request_answers_str}"
        elif self.request_type == "Difficult words":
            # explanations は不要
            options = ["all"]+list(range(3, 21))
            n_difficult_words = self.pane.select_slider(label=base_label + " (all, 3, 4, 5,...20)", options=options, value="all")
            return f"find {str(n_difficult_words)} difficult words"
        elif self.request_type == "Comprehension tasks":
            col1, col2 = self.pane.columns(2)
            n_comprehension = col1.slider(label=base_label, min_value=3, max_value=10, value=3)
            m_choice = col2.slider(label= "with M choices", min_value=2, max_value=6, value=4)
            return f"make {str(n_comprehension)} comprehension tasks with {m_choice} choices{request_answers_str}"
        elif self.request_type == "Discussion topics":
            col1, col2 = self.pane.columns(2)
            n_discussion_topics = col1.slider(label=base_label, min_value=3, max_value=10, value=3)
            m_minutes = col2.slider(label= "with M minutes", min_value=5, max_value=60, value=15, step=5)
            return f"suggest {str(n_discussion_topics)} discussion topics that is supposed to be finished in {m_minutes} minutes"
        elif self.request_type == "Word/phrase explanations":
            words_phrases = self.pane.text_input("Word/phrase")
            return f'explain the use of "{words_phrases}" and give some other examples'
        elif self.request_type == "Rewriting":
            return f'rewrite the text'
        elif self.request_type == "Summarizing":
            return f'summarize the text'
        else:
            return "Error"

st.header("ChatGPT Prompt Generator")
st.markdown("""
This app allows its users...
1. To generate prompts for ChatGPT to make questions for language learners.
1. To try sending the prompts to InstructGPT, a precedent model of ChatGPT.
""")

target_language = st.sidebar.header("PARAMETERS")
target_language = "of " + st.sidebar.radio(
    "Select target language",
    (
        'English',
        'Japanese',
    ))
reader_student = "for " + st.sidebar.radio(
    "Select readers/students level",
    options=(
        'Elementary learners',
        'Pre-intermediate learners',
        'Intermediate learners',
        'Advanced learners',
        'Native speakers',
        'Highly educated native speakers'
    ),).lower()

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

# FIXME: 解答の解説機能があまり機能していない.
answer_request = st.sidebar.radio("Do you need answers/explanations?", (
    "Yes, please.",
    "No, thank you.",
))
answer_request=answer_request[0]=="Y"
# answer_request = False

request = Request(request_type, st.sidebar, answer_request).query

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
prompt = " ".join(["Please", request, reader_student, target_language]) + reference_txt
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

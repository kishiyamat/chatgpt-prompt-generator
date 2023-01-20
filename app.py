import streamlit as st

st.header("ChatGPT Prompt Generator")

output_language = st.sidebar.header("PARAMETERS")
output_language = "of " + st.sidebar.radio(
    "Select output language",
    ('Japanese', 'English'))
reader_student = "for " + st.sidebar.radio(
    "Select readers/students level",
    options=(
        'Remedial learners',
        'Elementary learners',
        'Pre-intermediate learners',
        'Intermediate learners',
        'Advanced learners',
        'Native speakers',
        'Highly educated native speakers'
    ),).lower()


class Request:
    def __init__(self, request_type: str, pane)->None:
        self.request_type = request_type
        self.pane = pane
    @property
    def query(self)->str:
        if self.request_type == "Vocab quizzes":
            n_vocab_quizzes = self.pane.slider(label="N Vocab Quizzes",min_value=0, max_value=10)
            return str(n_vocab_quizzes)
        elif self.request_type == "Difficult words":
            n_difficult_words = self.pane.slider(label="N Difficult words",min_value=0, max_value=10)
            return str(n_difficult_words)
        elif self.request_type == "Comprehension tasks":
            col1, col2 = self.pane.columns(2)
            n_comprehension = col1.slider(label="N comprehension tasks",min_value=0, max_value=10)
            m_choice = col2.slider(label= "with M choices",min_value=0, max_value=10, value=4)
            return str(n_comprehension)
        else:
            return "Error"
         
st.sidebar.subheader("Select the request type")
request_type = st.sidebar.radio("Select request type", (
    "Vocab quizzes",
    "Comprehension tasks",
    "Difficult words",
    "Discussion topics",
))

request = Request(request_type, st.sidebar).query

# - [ ] 質問
#     - [ ] 単語の説明
#     - [ ] 語義の説明
#     - [ ] N個の用例の要求
#     - [ ] 文法性判断と説明
# - [ ] 書き換え
#     - [ ] 要約
#     - [ ] 固有名詞除外
#     - [ ] モード(Speaking/Writing)
# - [ ] 単語数(上限不明)
# - [ ] 参考文献
output = " ".join([request, reader_student, output_language])
st.text(output)
# st.text_input()

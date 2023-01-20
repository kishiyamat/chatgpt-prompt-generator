import streamlit as st

class Request:
    def __init__(self, request_type: str, pane)->None:
        self.request_type = request_type
        self.pane = pane
    @property
    def query(self)->str:
        # FIXME: N==1 の場合は複数形を直す(N>=3に限定しているので問題ない)
        base_label = f"N {self.request_type.lower()}"
        if self.request_type == "Vocab quizzes":
            n_vocab_quizzes = self.pane.slider(label=base_label, min_value=3, max_value=10, value=3)
            return f"make {str(n_vocab_quizzes)} vocab quizzes"
        elif self.request_type == "Difficult words":
            n_difficult_words = self.pane.slider(label=base_label, min_value=5, max_value=20, value=10)
            return f"find {str(n_difficult_words)} difficult words"
        elif self.request_type == "Comprehension tasks":
            col1, col2 = self.pane.columns(2)
            n_comprehension = col1.slider(label=base_label, min_value=3, max_value=10, value=3)
            m_choice = col2.slider(label= "with M choices", min_value=2, max_value=6, value=4)
            return f"make {str(n_comprehension)} comprehension tasks with {m_choice} choices"
        elif self.request_type == "Discussion topics":
            col1, col2 = self.pane.columns(2)
            n_discussion_topics = col1.slider(label=base_label, min_value=3, max_value=10, value=3)
            m_minutes = col2.slider(label= "with M minutes", min_value=3, max_value=60, value=15)
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
# output_language = "In " + st.sidebar.radio(
#     "Select output language",
#     ('Japanese', 'English')) + ","

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

request = Request(request_type, st.sidebar).query

reference = st.sidebar.radio(
    "Specify the reference",
    ("N/A", 'text')
    # ("N/A", 'text', "url")
    )

if reference=="N/A":
    reference_txt="."
elif reference=="text":
    text_input = st.sidebar.text_area(label="Text input", value="<Reference text comes here>")
    reference_txt=f", reading the following text.\n\n{text_input}"
elif reference=="url":
    url_input = st.sidebar.text_input(label="URL input", value="<Reference URL comes here>")
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
st.subheader("Output")
output = " ".join(["Please", request, reader_student, target_language]) + reference_txt
st.write(output)

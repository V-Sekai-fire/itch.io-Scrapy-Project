# MIT License

# Copyright (c) 2023-present K. S. Ernest (iFire) Lee

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import streamlit as st
import pprint
import marqo

st.set_page_config(
    page_title="Marqo Demo App",
    page_icon="favicon.png",
    layout="centered",
    initial_sidebar_state="collapsed",
    menu_items={},
)

template_attributes = [
    "author",
    "game_genre",
    "game_text",
    "num_ratings",
    "platform",
    "star_rating",
    "title",
    "title_url",
]

mq = marqo.Client(url="http://127.0.0.1:8882")
cwd = os.getcwd()
index = "itch-search"


def delete_index():
    try:
        mq.index(index).delete()
        st.success("Index successfully deleted.")
    except:
        st.error("Index does not exist.")


def save_uploadedfile(uploadedfile):
    with open(os.path.join(cwd, uploadedfile.name), "wb") as f:
        f.write(uploadedfile.getbuffer())
    return uploadedfile.name


def reset_state():
    st.session_state["results"] = {}
    st.session_state["page"] = -1


def create_filter_str(filter_list):
    filter_string = ""

    for filter in filter_list:
        filter_string = filter + ":true"
        filter_list.remove(filter)

    for field in filter_list:
        filter_string += f" AND label:({field})"

    print(filter_string)
    return filter_string

search_text, search_image_url, search_image = None, None, None
search_mode = st.radio(
    "", ("Text", "Image"), horizontal=True, on_change=reset_state
)
if search_mode == "Text":
    box_col, search_mode_col = st.columns([6, 1])
    with box_col:
        search_text = st.text_input("Text Search")

    with search_mode_col:
        search_text_mode = st.radio("Search mode", ("Tensor", "Lexical"))
else:
    image_input_col, image_type_col = st.columns([6, 1])

    with image_type_col:
        image_type = st.radio("Image type", ("Web", "Local"))

    with image_input_col:
        if image_type == "Web":
            search_image_url = st.text_input("Provide an Image URL")

        else:
            search_image = st.file_uploader("Upload an Image", type=["jpg", "jpeg", "png"])

with st.expander("Search Settings"):
    attr_col, filter_col = st.columns(2)
    with attr_col:
        searchable_attr = st.multiselect(
            "Searchable Attributes",
            template_attributes,
            default=template_attributes,
        )

    with filter_col:
        filtering = st.multiselect(
            "Pre-filtering Options", ["Action", "Visual Novel"], default=None
        )

search_btn = st.button("Search")

if 'results' not in st.session_state:
    st.session_state['results'] = {}

if 'page' not in st.session_state:
    st.session_state['page'] = -1

if (
    (search_image is not None) or (search_image_url) or (search_text)
) and search_btn:
    if search_text != "" and search_text != None:
        results = mq.index(index).search(
            q=search_text,
            search_method=search_text_mode.upper(),
            limit=30,
        )

    elif search_image_url != "" and search_image_url != None:
        results = mq.index(index).search(
            search_image_url,
            limit=30,
        )

    else:
        uploaded_img_name = save_uploadedfile(search_image)

        uploaded_img_path = f"http://host.docker.internal:8222/{uploaded_img_name}"
        print(uploaded_img_path)

        results = mq.index(index).search(
            uploaded_img_path,
            filter_string=create_filter_str(filtering),
            searchable_attributes=[i.lower() for i in searchable_attr],
            limit=30,
        )

    pprint.pprint(results)

    st.session_state["results"] = results

    if st.session_state["results"]["hits"]:
        st.session_state["page"] = 0
    else:
        st.session_state["page"] = -1

    if st.session_state["page"] > -1:
        prev_col, page_col, next_col = st.columns([1, 9, 1])
        with prev_col:
            prev_btn = st.button("Prev")
            if prev_btn and (st.session_state["page"] > 0):
                st.session_state["page"] -= 1

        with next_col:
            next_btn = st.button("Next")
            if next_btn and (st.session_state["page"] < 2):
                st.session_state["page"] += 1

        with page_col:
            st.markdown(
                '<div style="text-align: center"> {}</div>'.format(
                    "Page " + str(st.session_state["page"] + 1)
                ),
                unsafe_allow_html=True,
            )

    if st.session_state["results"] != {}:
      if st.session_state["results"]["hits"]:
        st.write("Results (Top 30):")
        col = st.columns(5)
        for hit in enumerate(st.session_state["results"]["hits"]):
            for attr in template_attributes:
                attr_value = hit[1].get(attr, None)
                if attr_value is not None:
                    if attr == "title_url":
                        st.markdown(
                            "[{0}]({1})".format(hit[1]["title"], attr_value), unsafe_allow_html=True
                        )
                    else:
                        st.write(f"{attr}: {attr_value}")
else:
    st.write("No results")
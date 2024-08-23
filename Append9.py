import streamlit as st
import os
import pickle
import uuid
from st_pages import Page, show_pages
from main7 import main

@st.experimental_dialog("Confirm Delete section")
def confirm_delete_section(section_name):
    st.write(f"Are you sure you want to delete the section '{section_name}' and all its pages?")
    if st.button("Yes, delete section"):
        st.session_state.section_delete_confirmed = True
        st.rerun()
    if st.button("No, cancel"):
        st.session_state.section_delete_confirmed = False
        st.rerun()

@st.experimental_dialog("Confirm Delete page")
def confirm_delete_page(page_name):
    st.write(f"Are you sure you want to delete the page '{page_name}'?")
    if st.button("Yes, delete page"):
        st.session_state.page_delete_confirmed = True
        st.rerun()
    if st.button("No, cancel"):
        st.session_state.page_delete_confirmed = False
        st.rerun()

# Load or initialize pages
if os.path.exists("pages.pkl"):
    with open("pages.pkl", "rb") as file:
        pages = pickle.load(file)
else:
    pages = [Page("D:\\Akshay Files\\AI_Demo\\zoho.py", "Zoho", "🏠")]

if os.path.exists("dict.pkl"):
    with open("dict.pkl", "rb") as file:
        dict = pickle.load(file)
else:
    dict = {("D:\\Akshay Files\\Multi_page\\Dynamicsite\\append9.py", "Append", ""): []}

# Function to save pages
def save_pages(pages):
    with open("pages.pkl", "wb") as file:
        pickle.dump(pages, file)
    show_pages(pages)

def is_duplicate_path_or_name(path, name, exclude_path=None, exclude_name=None):
    for key, pages_list in dict.items():
        # Check for duplicate section paths and names
        if (key[0] == path or key[1] == name) and (key[0] != exclude_path or key[1] != exclude_name):
            return True
        # Check for duplicate page paths and names within sections
        for page in pages_list:
            if (page.path == path or page.name == name) and (page.path != exclude_path or page.name != exclude_name):
                return True
    return False

def save_dict(dict):
    with open("dict.pkl", "wb") as file:
        pickle.dump(dict, file)

# Function to add sections and pages to the pages list from the dictionary
def add_sections_and_pages(dict):
    pages = []
    for section, pages_list in dict.items():
        pages.append(Page(section[0], section[1], section[2]))
        pages.extend(pages_list)
    return pages

# Streamlit app layout
st.title("Section and Page Management")
tabs = ["Create Section", "Update Section", "Delete Section", "Create Page", "Update Page", "Delete Page"]
tab0, tab1, tab2, tab3, tab4, tab5 = st.tabs(tabs)

with tab0:
    st.header("Create Section")
    section_name = st.text_input("Enter section name")
    section_file = st.file_uploader("Upload Python file for section", type="py")
    if st.button("Create Section", key="create_section"):
        if section_name and section_file:
            section_path = os.path.join("D:\\Akshay Files\\Multi_page\\Dynamicsite", f"{uuid.uuid4()}.py")
            if not is_duplicate_path_or_name(section_path, section_name):
                with open(section_path, "wb") as f:
                    f.write(section_file.getbuffer())
                dict[(section_path, section_name, "")] = []
                save_dict(dict)
                pages = add_sections_and_pages(dict)
                save_pages(pages)
                st.success(f"Section '{section_name}' created successfully.")
            else:
                st.error(f"File name/path already exists")

with tab2:
    st.header("Delete Section")
    section_choice = st.selectbox("Choose a section to delete",
                                  [(key[0], key[1]) for key in dict.keys() if key[2] == ""], key="delete_section_selectbox")

    if 'delete_confirm' not in st.session_state:
        st.session_state.delete_confirm = False

    if st.button("Delete Section", key="delete_section"):
        st.session_state.delete_confirm = True

    if st.session_state.delete_confirm:
        confirm_delete_section(section_choice[1])

    if 'section_delete_confirmed' in st.session_state and st.session_state.section_delete_confirmed:
        # Remove the section and its pages
        dict.pop((section_choice[0], section_choice[1], ""))
        save_dict(dict)
        pages = add_sections_and_pages(dict)
        save_pages(pages)
        st.success(f"Section '{section_choice[1]}' deleted successfully.")
        st.session_state.delete_confirm = False
        st.session_state.section_delete_confirmed = False
    elif 'section_delete_confirmed' in st.session_state and not st.session_state.section_delete_confirmed:
        st.info("Section deletion cancelled.")
        st.session_state.delete_confirm = False

with tab1:
    st.header("Update Section")
    section_choice = st.selectbox("Choose a section to update",
                                  [(key[0], key[1]) for key in dict.keys() if key[2] == ""], key="update_section_selectbox")
    new_name = st.text_input("Enter new section name", value=section_choice[1])
    new_path_file = st.file_uploader("Upload new Python file for section", type="py")

    if st.button("Update Section", key="update_section"):
        new_path = os.path.join("D:\\Akshay Files\\Multi_page\\Dynamicsite", f"{uuid.uuid4()}.py")
        if new_name and new_path_file:
            if not is_duplicate_path_or_name(new_path, new_name, section_choice[0], section_choice[1]):
                with open(new_path, "wb") as f:
                    f.write(new_path_file.getbuffer())
                dict[(new_path, new_name, "")] = dict.pop((section_choice[0], section_choice[1], ""))
                save_dict(dict)
                pages = add_sections_and_pages(dict)
                save_pages(pages)
                main()
                st.success(
                    f"Section '{section_choice[1]}' updated to '{new_name}' with new path '{new_path}' successfully.")
            else:
                st.error(f"File name/path already exists")

with tab3:
    st.header("Create Page")
    sections = [(key[0], key[1]) for key in dict.keys() if key[2] == ""]
    section_choice = st.selectbox("Choose a section", sections, key="create_page_section_selectbox")
    page_name = st.text_input("Enter page name")
    page_file = st.file_uploader("Upload Python file for page", type="py")
    page_icon = st.text_input("Enter page icon")
    if st.button("Create Page", key="create_page"):
        if page_name and page_file:
            page_path = os.path.join("D:\\Akshay Files\\Multi_page\\Dynamicsite", f"{uuid.uuid4()}.py")
            if not is_duplicate_path_or_name(page_path, page_name):
                with open(page_path, "wb") as f:
                    f.write(page_file.getbuffer())
                dict[(section_choice[0], section_choice[1], "")].append(Page(page_path, page_name, page_icon))
                save_dict(dict)
                pages = add_sections_and_pages(dict)
                save_pages(pages)
                st.success(f"Page '{page_name}' created successfully.")
            else:
                st.error(f"File name already exists")

with tab4:
    st.header("Update Page")
    section_choice = st.selectbox("Choose a section",
                                  [(key[0], key[1]) for key in dict.keys() if key[2] == ""], key="update_page_section_selectbox")
    if section_choice:
        page_choice = st.selectbox("Choose a page to update",
                                   [(page.path, page.name, page.icon) for page in dict[(section_choice[0], section_choice[1], "")]],
                                   key="update_page_selectbox")
        if page_choice:
            new_name = st.text_input("Enter new page name", value=page_choice[1])
            new_path_file = st.file_uploader("Upload new Python file for page", type="py")
            new_icon = st.text_input("Enter new page icon", value=page_choice[2])
            if st.button("Update Page", key="update_page_button"):
                new_path = os.path.join("D:\\Akshay Files\\Multi_page\\Dynamicsite", f"{uuid.uuid4()}.py")
                if new_name and new_path_file:
                    if not is_duplicate_path_or_name(new_path, new_name, page_choice[0], page_choice[1]):
                        with open(new_path, "wb") as f:
                            f.write(new_path_file.getbuffer())
                        # Update the existing page in the dict
                        for key, pages_list in dict.items():
                            for idx, page in enumerate(pages_list):
                                if page.path == page_choice[0] and page.name == page_choice[1] and page.icon == page_choice[2]:
                                    pages_list[idx] = Page(new_path, new_name, new_icon)
                        save_dict(dict)
                        pages = add_sections_and_pages(dict)
                        save_pages(pages)
                        main()
                        st.success(
                            f"Page '{page_choice[1]}' updated to '{new_name}' with new path '{new_path}' and new icon '{new_icon}' successfully.")
                    else:
                        st.error(f"File name/path already exists")

with tab5:
    st.header("Delete Page")
    sections = [(key[0], key[1]) for key in dict.keys() if key[2] == ""]
    section_choice = st.selectbox("Choose a section", sections, key="delete_page_section_selectbox")

    if section_choice:
        pages_in_section = [(page.path, page.name) for page in dict[(section_choice[0], section_choice[1], "")]]
        page_choice = st.selectbox("Choose a page to delete", pages_in_section, key="delete_page_selectbox")

        if page_choice:
            if 'page_delete_confirm' not in st.session_state:
                st.session_state.page_delete_confirm = False
            if 'page_delete_confirmed' not in st.session_state:
                st.session_state.page_delete_confirmed = False

            if st.button("Delete Page", key="delete_page"):
                st.session_state.page_delete_confirm = True

            if st.session_state.page_delete_confirm:
                confirm_delete_page(page_choice[1])

            if 'page_delete_confirmed' in st.session_state and st.session_state.page_delete_confirmed:
                dict[(section_choice[0], section_choice[1], "")] = [
                    page for page in dict[(section_choice[0], section_choice[1], "")]
                    if page.path != page_choice[0]
                ]
                save_dict(dict)
                pages = add_sections_and_pages(dict)
                save_pages(pages)
                st.success(f"Page '{page_choice[1]}' deleted successfully.")
                st.session_state.page_delete_confirm = False
                st.session_state.page_delete_confirmed = False
            elif 'page_delete_confirmed' in st.session_state and not st.session_state.page_delete_confirmed:
                st.info("Page deletion cancelled.")
                st.session_state.page_delete_confirm = False

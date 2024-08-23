import streamlit as st
import os
import pickle
from st_pages import Page, Section, show_pages, hide_pages, show_pages_from_config, add_page_title
# Page class definition
# class Page:
#     def __init__(self, path, name, icon):
#         self.path = path
#         self.name = name
#         self.icon = icon
#
#     def __repr__(self):
#         return f"Page({self.path}, {self.name}, {self.icon})"
def main():
    # Load or initialize pages
    if os.path.exists("pages.pkl"):
        with open("pages.pkl", "rb") as file:
            pages = pickle.load(file)
    else:
        pages = [Page("D:\\Akshay Files\\Multi_page\\Dynamicsite\\append9.py","Append","")]
        with open("pages.pkl", "wb") as file:
            pickle.dump(pages, file)
    show_pages(pages)
    st.experimental_rerun()
if __name__ == "__main__":
    main()
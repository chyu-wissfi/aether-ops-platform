#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author : chyu-wissfi
@Email : chyu.wissfi@gmail.com
@File   : faiss_local_data.py
"""
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.vectorstores.faiss import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

# 数据源的位置需要根据实际数据位置做修改
loader = DirectoryLoader(path="./storage/vector_store", glob="**/[!.]*")

text_splitter = RecursiveCharacterTextSplitter(
    separators=[
        "\n\n",
        "\n",
        "。|！|？",
        "\.\s|\!\s|\?\s",  # 英文标点符号后面通常需要加空格
        "；|;\s",
        "，|,\s",
        " ",
        ""
    ],
    is_separator_regex=True,
    chunk_size=500,
    chunk_overlap=50,
    add_start_index=True,
)

documents = loader.load_and_split(text_splitter)

db = FAISS.from_documents(
    documents=documents,
    embedding=OpenAIEmbeddings(model="text-embedding-3-small")
)

# 向量数据库的位置需要根据实际的位置做修改
db.save_local(folder_path="./internal/core/vector_store", index_name="index")

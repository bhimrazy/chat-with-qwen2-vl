<div align="center">
    <h3 style="margin-bottom:-55px;margin-left:55px;color:#6332e5">Chat with</h3>
    <img src="https://qianwen-res.oss-accelerate-overseas.aliyuncs.com/Qwen2-VL/qwen2VL_logo.png" width="400"/>
</div

## Overview
[**Qwen2-VL **](https://huggingface.co/Qwen/Qwen2-VL-7B-Instruct) is the latest version of the vision language models in the Qwen model familities.

This model enables multi-frame image understanding, image comparison, multi-image summarization/storytelling, and video summarization, which have broad applications in office scenarios.

## Getting Started

Follow these steps to set up and run the project:

### 1. Install Dependencies

Ensure all necessary packages are installed by running:

```bash
pip install -r requirements.txt
```

### 2. Start the API Server

Launch the API server powered by [LitServe](https://github.com/Lightning-AI/LitServe):

```bash
python server.py
```

### 3. Launch the Streamlit App

Start the Streamlit application with the following command:

```bash
streamlit run app.py
```

## About

This project is developed and maintained with ❤️ by [Bhimraj Yadav](https://github.com/bhimrazy).


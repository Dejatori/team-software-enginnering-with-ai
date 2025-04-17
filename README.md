# 📘 Team Software Engineering with AI

Welcome to the **"Team Software Engineering With AI"** repository! 🌟 This repository contains
my notes, exercises, and code examples from the course, designed to help developers understand 
and apply generative AI concepts in software development to work in teams. 🚀

---

## 📑 Table of Contents

- [📘 Introduction to Team Software Engineering With AI](#-team-software-enginnering-with-ai)
    - [📑 Table of Contents](#-table-of-contents)
    - [📥 Installation](#-installation)
    - [📖 Usage](#-usage)
    - [🤝 Contributing](#-contributing)
    - [📜 License](#-license)
    - [📞 Support/Contact](#-supportcontact)
    - [🙏 Acknowledgments](#-acknowledgments)

---

## 📥 Installation

To get started with this repository, follow these steps:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Dejatori/team-software-enginnering-with-ai
   cd team-software-enginnering-with-ai
   ```

2. **Set up a Python environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   # or use conda
   conda create -n generative-ai python=3.13.2
   conda activate generative-ai
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   # or use conda
   conda install -c conda-forge -c anaconda --file requirements.txt
   ```

4. **Launch the Jupyter Notebook**:
   ```bash
   jupyter notebook
   ```

You're all set! 🎉

---

## 📖 Usage

This repository provides examples and exercises to help you understand and apply generative AI concepts in software development. Here's how you can use it:

1. **Explore the Code**:
   - Navigate through the `module_1`, `module_2`, and `module_3` directories to find R and Python examples.
   - Review the `code_snippets.py` and `tasks.R` files for practical implementations.

2. **Run the Examples**:
   - Use the provided Jupyter Notebooks to experiment with the Python code.
   - For R scripts, ensure you have R installed and run the scripts using an R environment.

3. **Generate Documentation**:
   - For Python code, use Sphinx to generate documentation:
     ```bash
     cd module_2/docs
     make html
     ```
     Open the generated HTML files in your browser to view the documentation.

4. **Test the API**:
   - Use the `tests.http` file in `module_1` to test the Flask API endpoints with tools like Postman or VS Code's REST Client extension.

5. **Modify and Extend**:
   - Add your own tasks or modify the existing ones to suit your learning goals.
   - Use the `prompts.md` file for ideas on how to enhance the code with AI-driven improvements.

---

## 🤝 Contributing

We welcome contributions to this repository! 🛠️ Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add an amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📜 License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT). 📝  
![MIT License Badge](https://img.shields.io/badge/License-MIT-blue.svg)

---

## 🙏 Acknowledgments

A big thank you to:

- DeepLearning.AI, for this course of **"Introduction to Generative AI for Software Development"**. 🎓
- The Instructor [Laurence Moroney](https://www.linkedin.com/in/laurence-moroney/) for their excellent teaching
and insights. 👨‍🏫
- Open-source libraries and tools like Python, Jupyter, and NLTK that made this project possible. 🛠️
- The amazing developer community for their support and inspiration. 🌟

---

Happy learning and coding! 🎉
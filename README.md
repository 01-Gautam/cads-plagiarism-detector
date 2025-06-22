# 🤖 CADS: Code Authenticity Detection System

<!-- Larger Streamlit badge -->
<a href="https://cads-plagiarism-detector-pt7v39zijm5niyo3mwly67.streamlit.app/" target="_blank">
  <img src="https://static.streamlit.io/badges/streamlit_badge_black_white.svg" alt="Streamlit App" style="height:30px;">
</a>

**CADS** is a sophisticated, web-based tool designed to analyze and detect similarities in code files. Powered by an advanced fingerprinting algorithm and a modern, immersive user interface built with Streamlit, CADS provides a seamless experience for ensuring code authenticity.

---

## ✨ Key Features

*   **Modern & Immersive UI**: A visually appealing interface with gradient backgrounds, animated elements, and a clean, tab-based layout.
*   **Flexible File Support**: Upload and analyze a wide variety of code files, including `.c`, `.py`, `.java`, and more. The system smartly validates that all files in a batch are of the same type.
*   **Interactive Analytics Dashboard**:
    *   **Highest Similarity Metric**: Instantly see the most critical plagiarism score.
    *   **Risk Level Assessment**: Automatically categorizes the highest similarity into "Low," "Medium," or "High" risk.
    *   **Similarity Distribution Histogram**: Get a high-level overview of the plagiarism landscape across all comparisons.
    *   **Similarity Matrix Heatmap**: A powerful grid that visualizes the similarity score for every file-to-file comparison, making it easy to spot clusters of cheating.
*   **Detailed HTML Reports**: Generate and download a comprehensive report with side-by-side code comparisons and highlighted plagiarism areas.
*   **Analysis History**: Track your detection jobs over time with a historical log and a trend chart showing the maximum similarity found in each batch.
*   **Built for Simplicity**: A clear, three-step process makes it incredibly easy to use: Upload -> Detect -> Analyze.

---

## ⚙️ How It Works

CADS doesn't just look for copied lines; it analyzes the underlying structure of the code using a proven technique called **fingerprinting**.

1.  **Tokenization**: The source code is broken down into a sequence of fundamental units, or "tokens."
2.  **K-gram Analysis**: The system creates overlapping sequences of these tokens (called k-grams).
3.  **Winnowing Algorithm**: To improve efficiency without sacrificing accuracy, a winnowing algorithm is used to select a smaller, representative set of fingerprints from the k-grams.
4.  **Comparison**: Finally, the system compares the fingerprint sets from all files to calculate a similarity score for each pair.

---

## 🚀 Getting Started (Local Setup)

To run this project on your own machine, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/01-Gautam/cads-plagiarism-detector.git
    cd cads-plagiarism-detector
    ```

2.  **Install the required dependencies:**
    Make sure you have Python 3.8+ installed. Then, run:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the Streamlit app:**
    ```bash
    streamlit run app.py
    ```
    The application will open in your web browser!

---

## ❤️ Developed by Team Code Explorers

---
## <span style="font-size:1.5em">👥 About Our Team</span>

We are <b>Team Code Explorers</b> — passionate about code quality, academic integrity, and building immersive web tools!

<br>

## <span style="font-size:1.5em">👥 About Our Team</span>

We are <b>Team Code Explorers</b> — passionate about code quality, academic integrity, and building immersive web tools!

<br>

<div align="center">

<table width="80%">
  <tr>
    <th style="font-size:1.1em; min-width: 180px;">Role</th>
    <th style="font-size:1.1em; min-width: 220px;">Name</th>
    <th style="font-size:1.1em; min-width: 220px;">GitHub</th>
  </tr>
  <tr>
    <td><span style="font-size:1.3em;">👑</span> <b>Team Leader</b></td>
    <td><b><span style="font-size:1.1em;">Sambhav Jain</span></b></td>
    <td>
      <a href="https://github.com/Sambhav1501">
        <img src="https://img.shields.io/badge/GitHub-Profile-blue?logo=github&style=for-the-badge" alt="Sambhav Jain GitHub"/>
      </a>
    </td>
  </tr>
  <tr>
    <td><span style="font-size:1.3em;">🧑‍💻</span> <b>Member 1</b></td>
    <td><b><span style="font-size:1.1em;">Gautam Tripathi</span></b></td>
    <td>
      <a href="https://github.com/01-Gautam">
        <img src="https://img.shields.io/badge/GitHub-Profile-blue?logo=github&style=for-the-badge" alt="Gautam Tripathi GitHub"/>
      </a>
    </td>
  </tr>
  <tr>
    <td><span style="font-size:1.3em;">🧑‍💻</span> <b>Member 2</b></td>
    <td><b><span style="font-size:1.1em;">Mohd Adeeb Ansari</span></b></td>
    <td>
      <a href="https://github.com/adeebansari110">
        <img src="https://img.shields.io/badge/GitHub-Profile-blue?logo=github&style=for-the-badge" alt="Mohd Adeeb Ansari GitHub"/>
      </a>
    </td>
  </tr>
</table>

</div>

<br>
---

> **Connect with us on GitHub and check out our other projects!**

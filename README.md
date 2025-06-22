# 🤖 CADS: Code Authenticity Detection System

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://YOUR_STREAMLIT_APP_URL_HERE)

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

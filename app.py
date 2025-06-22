import streamlit as st
import tempfile
import os
import shutil
import time
import json
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from datetime import datetime
import base64
from pathlib import Path
from copydetect import detector, CopyDetector, CodeFingerprint, compare_files

# Configure matplotlib and seaborn styling
plt.style.use('default')
sns.set_palette("husl")
sns.set_style("whitegrid")
plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['axes.facecolor'] = 'white'

# Page configuration with custom theme
st.set_page_config(
    page_title="CADS: Code Authenticity Detection System",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for immersive design
st.markdown("""
<style>
    /* Modern gradient background */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
    }
    
    /* Custom styling for main content */
    .main .block-container {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(10px);
    }
    
    /* Animated header */
    .main-header {
        background: linear-gradient(90deg, #667eea, #764ba2, #f093fb);
        background-size: 200% 200%;
        animation: gradientShift 3s ease infinite;
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Custom button styling */
    .stButton > button {
        background: linear-gradient(90deg, #667eea, #764ba2);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-weight: bold;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.6);
    }
    
    /* File uploader styling */
    .stFileUploader > div {
        border: 2px dashed #667eea;
        border-radius: 15px;
        padding: 2rem;
        background: rgba(102, 126, 234, 0.05);
        transition: all 0.3s ease;
    }
    
    .stFileUploader > div:hover {
        border-color: #764ba2;
        background: rgba(102, 126, 234, 0.1);
    }
    
    /* Progress bar styling */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #667eea, #764ba2);
    }
    
    /* Metric cards */
    .metric-card {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
        transition: transform 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Success message styling */
    .success-message {
        background: linear-gradient(90deg, #56ab2f, #a8e6cf);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        animation: slideIn 0.5s ease;
    }
    
    @keyframes slideIn {
        from { transform: translateX(-100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    /* Warning message styling */
    .warning-message {
        background: linear-gradient(90deg, #f093fb, #f5576c);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    /* Info message styling */
    .info-message {
        background: linear-gradient(90deg, #4facfe, #00f2fe);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'uploaded_files' not in st.session_state:
    st.session_state.uploaded_files = []
if 'detection_results' not in st.session_state:
    st.session_state.detection_results = None
if 'analysis_history' not in st.session_state:
    st.session_state.analysis_history = []
if 'current_step' not in st.session_state:
    st.session_state.current_step = 0

# Sidebar configuration - Simplified
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 1rem;">
        <h2>CADS</h2>
        <p style="color: white; opacity: 0.8;">Code Authenticity Detection System</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 📈 Quick Stats")
    if st.session_state.analysis_history:
        total_analyses = len(st.session_state.analysis_history)
        st.metric("Total Analyses", total_analyses)
    else:
        st.info("No analyses yet. Upload files to get started!")
    
    st.markdown("### 🚀 How It Works")
    st.markdown("""
    1. **Upload** code files of the same type
    2. **Click** detect button
    3. **View** results instantly
    4. **Download** detailed reports
    """)

# Main content
st.markdown("""
<div class="main-header">
    <h1>CADS</h1>
    <p style="font-size: 1.2rem; margin: 0;">Code Authenticity Detection System</p>
    <p style="opacity: 0.8;">Upload your code files and detect similarities instantly</p>
</div>
""", unsafe_allow_html=True)

# Main tabs
tab1, tab2, tab3, tab4 = st.tabs(["🚀 Detection", "📊 Analytics & Report", "📋 History", "ℹ️ Help"])

with tab1:
    st.markdown("### 📁 Upload Code Files")
    st.markdown("Upload two or more code files to detect similarities. **All files in a batch must have the same extension.**")
    
    # File uploader with enhanced styling
    uploaded_files = st.file_uploader(
        "Choose code files to analyze",
        type=["py", "c", "cpp", "java", "js", "ts", "php", "rb", "go", "rs", "txt"],
        accept_multiple_files=True,
        help="Upload any supported code file type. All files must have the same extension."
    )
    
    if uploaded_files:
        # File type validation
        first_ext = uploaded_files[0].name.split('.')[-1] if '.' in uploaded_files[0].name else ''
        all_same_type = all((f.name.split('.')[-1] if '.' in f.name else '') == first_ext for f in uploaded_files)
        
        if not all_same_type:
            st.error("❌ Mismatched file types. Please upload files with the same extension (e.g., all `.c` or all `.py`).")
        elif len(uploaded_files) < 2:
            st.warning("⚠️ Please upload at least two files to compare.")
        else:
            st.session_state.uploaded_files = uploaded_files
            
            # File information display
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Files Uploaded", len(uploaded_files))
            with col2:
                total_size = sum(f.size for f in uploaded_files)
                st.metric("Total Size", f"{total_size / 1024:.1f} KB")
            with col3:
                st.metric("File Type", f".{first_ext}")

            # File list with details
            st.markdown("### 📋 Uploaded Files")
            file_data = []
            for i, file in enumerate(uploaded_files):
                file_data.append({
                    'Name': file.name,
                    'Size (KB)': f"{file.size / 1024:.1f}",
                    'Type': file.name.split('.')[-1].upper(),
                    'Status': '✅ Ready'
                })
            
            df_files = pd.DataFrame(file_data)
            st.dataframe(df_files, use_container_width=True)
            
            # Detection button with progress
            if st.button("🚀 Run Plagiarism Detection", type="primary"):
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                try:
                    status_text.text("📁 Preparing files for analysis...")
                    progress_bar.progress(20)
                    
                    with tempfile.TemporaryDirectory() as temp_dir:
                        test_folder = os.path.join(temp_dir, "test")
                        os.makedirs(test_folder, exist_ok=True)
                        
                        for uploaded_file in uploaded_files:
                            file_path = os.path.join(test_folder, uploaded_file.name)
                            with open(file_path, "wb") as f:
                                f.write(uploaded_file.getbuffer())
                        
                        progress_bar.progress(40)
                        status_text.text("🔍 Initializing detection engine...")
                        
                        detector_instance = CopyDetector(
                            test_dirs=[test_folder],
                            ref_dirs=[test_folder],
                            extensions=[first_ext],
                            noise_t=25,
                            guarantee_t=25,
                            display_t=0.33
                        )
                        
                        detector_instance.run()

                        html_report = detector_instance.generate_html_report(output_mode="return")
                        
                        if html_report is None:
                            st.error("The plagiarism detector failed to generate an HTML report. This can happen if no files were found to compare. Please ensure you have uploaded at least two valid files.")

                        cleaned_html_report = html_report
                        if cleaned_html_report:
                            all_temp_files = set(detector_instance.test_files + detector_instance.ref_files)
                            for full_path_str in all_temp_files:
                                if full_path_str:
                                    filename_only = os.path.basename(full_path_str)
                                    cleaned_html_report = cleaned_html_report.replace(full_path_str, filename_only)
                                    posix_path = str(Path(full_path_str).as_posix())
                                    cleaned_html_report = cleaned_html_report.replace(posix_path, filename_only)
                        
                        progress_bar.progress(80)
                        status_text.text("📊 Processing results...")
                        
                        scores = []
                        if hasattr(detector_instance, 'similarity_matrix') and detector_instance.similarity_matrix.size > 0:
                            similarity_matrix = detector_instance.similarity_matrix[:, :, 0]
                            for i, test_file in enumerate(detector_instance.test_files):
                                for j, ref_file in enumerate(detector_instance.ref_files):
                                    if i != j and similarity_matrix[i, j] >= 0:
                                        similarity_percent = similarity_matrix[i, j] * 100
                                        test_filename = os.path.basename(test_file)
                                        ref_filename = os.path.basename(ref_file)
                                        scores.append((test_filename, ref_filename, similarity_percent))

                        max_similarity_percent = 0
                        
                        if scores:
                            similarities_percent = [score[2] for score in scores]
                            max_similarity_percent = max(similarities_percent)
                            
                            st.session_state.analysis_history.append({
                                'timestamp': datetime.now().isoformat(),
                                'files_analyzed': len(uploaded_files),
                                'max_similarity': max_similarity_percent,
                                'total_comparisons': len(scores)
                            })
                            
                            st.markdown(f"""
                            <div class="success-message">
                                <h3>🎉 Detection Complete!</h3>
                                <p>Analyzed {len(uploaded_files)} files with {len(scores)} comparisons.</p>
                                <p>Highest Similarity Found: <strong>{max_similarity_percent:.2f}%</strong></p>
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.warning("No similarities detected above the threshold.")

                        st.session_state.detection_results = {
                            'scores': scores,
                            'max_similarity': max_similarity_percent,
                            'total_comparisons': len(scores),
                            'timestamp': datetime.now().isoformat(),
                            'html_report': cleaned_html_report
                        }

                        progress_bar.progress(100)
                        status_text.text("✅ Analysis completed successfully!")
                
                except Exception as e:
                    st.error(f"❌ Error during detection: {str(e)}")
                    progress_bar.progress(0)

with tab2:
    st.markdown("### 📊 Interactive Analytics & Report")
    
    if 'detection_results' not in st.session_state or st.session_state.detection_results is None:
        st.info("Run a detection analysis first to view analytics and reports.")
    else:
        results = st.session_state.detection_results
        
        analytics_tab, report_tab = st.tabs(["📊 Visual Analytics", "📄 Report"])

        with analytics_tab:
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"""
                <div class="metric-card">
                    <h3>🔥 Highest Similarity</h3>
                    <h2>{results['max_similarity']:.1f}%</h2>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="metric-card">
                    <h3>🔍 Comparisons</h3>
                    <h2>{results['total_comparisons']}</h2>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                risk_level = "High" if results['max_similarity'] > 70 else "Medium" if results['max_similarity'] > 30 else "Low"
                risk_color = "#ff6b6b" if risk_level == "High" else "#feca57" if risk_level == "Medium" else "#48dbfb"
                st.markdown(f"""
                <div class="metric-card" style="background: linear-gradient(135deg, {risk_color}, {risk_color}dd);">
                    <h3>⚠️ Risk Level</h3>
                    <h2>{risk_level}</h2>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("### 📊 Similarity Distribution")
            
            if results['scores']:
                similarities_percent = [score[2] for score in results['scores']]
                
                fig_hist, ax_hist = plt.subplots(figsize=(10, 6))
                sns.histplot(similarities_percent, bins=20, color='#667eea', alpha=0.7, edgecolor='black')
                ax_hist.set_title("Distribution of Code Similarity Scores", fontsize=16, fontweight='bold')
                ax_hist.set_xlabel("Similarity (%)", fontsize=12)
                ax_hist.set_ylabel("Number of Comparisons", fontsize=12)
                ax_hist.grid(True, alpha=0.3)
                
                mean_sim_percent = np.mean(similarities_percent)
                median_sim_percent = np.median(similarities_percent)
                ax_hist.axvline(mean_sim_percent, color='red', linestyle='--', label=f'Mean: {mean_sim_percent:.1f}%')
                ax_hist.axvline(median_sim_percent, color='green', linestyle='--', label=f'Median: {median_sim_percent:.1f}%')
                ax_hist.legend()
                
                plt.tight_layout()
                st.pyplot(fig_hist)
                
                st.markdown("### 🔥 Similarity Heatmap")
                
                file_pairs = [(score[0], score[1], score[2]) for score in results['scores']]
                unique_files = sorted(list(set([f for pair in file_pairs for f in pair[:2]])))
                
                similarity_matrix = pd.DataFrame(index=unique_files, columns=unique_files, dtype=float)
                for file1, file2, similarity in file_pairs:
                    similarity_matrix.loc[file1, file2] = similarity
                    similarity_matrix.loc[file2, file1] = similarity
                
                fig_heatmap, ax_heatmap = plt.subplots(figsize=(10, 8))
                mask = np.eye(len(unique_files), dtype=bool)
                
                sns.heatmap(similarity_matrix.fillna(0), annot=True, cmap='RdYlBu_r', fmt='.1f', cbar=True, 
                           xticklabels=unique_files, yticklabels=unique_files, mask=mask, square=True,
                           linewidths=0.5, cbar_kws={'label': 'Similarity (%)'})
                
                ax_heatmap.set_title("Code File Similarity Matrix", fontsize=16, fontweight='bold')
                ax_heatmap.set_xlabel("File 1", fontsize=12)
                ax_heatmap.set_ylabel("File 2", fontsize=12)
                plt.xticks(rotation=45, ha='right')
                plt.yticks(rotation=0)
                plt.tight_layout()
                st.pyplot(fig_heatmap)
            
            st.markdown("### 📋 Detailed Results")
            if results['scores']:
                detailed_data = []
                for file1, file2, similarity in results['scores']:
                    risk = "High" if similarity > 70 else "Medium" if similarity > 30 else "Low"
                    detailed_data.append({
                        'File 1': file1,
                        'File 2': file2,
                        'Similarity (%)': f"{similarity:.2f}",
                        'Risk Level': risk,
                        'Status': '⚠️ High Risk' if similarity > 70 else '⚡ Medium Risk' if similarity > 30 else '✅ Low Risk'
                    })
                
                df_detailed = pd.DataFrame(detailed_data)
                st.dataframe(df_detailed, use_container_width=True)
                
                csv = df_detailed.to_csv(index=False)
                st.download_button(
                    label="📥 Download Results (CSV)",
                    data=csv,
                    file_name=f"plagiarism_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
            else:
                st.info("No plagiarism detected.")

        with report_tab:
            st.markdown("### 📄 Generated HTML Report")

            if results.get('html_report'):
                st.download_button(
                    label="📥 Download HTML Report",
                    data=results['html_report'],
                    file_name=f"plagiarism_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html",
                    mime="text/html"
                )
                st.components.v1.html(results['html_report'], height=800, scrolling=True)
            else:
                st.warning("No visual report was generated. This typically happens when no similarities are found between the files, or if an error occurred during report creation.")

with tab3:
    st.markdown("### 📋 Analysis History")
    
    if st.session_state.analysis_history:
        history_data = []
        for entry in st.session_state.analysis_history:
            timestamp = datetime.fromisoformat(entry['timestamp'])
            history_data.append({
                'Date': timestamp.strftime('%Y-%m-%d %H:%M'),
                'Files Analyzed': entry['files_analyzed'],
                'Max Similarity (%)': f"{entry['max_similarity']:.2f}",
                'Comparisons': entry['total_comparisons']
            })
        
        df_history = pd.DataFrame(history_data)
        st.dataframe(df_history, use_container_width=True)
        
        if len(history_data) > 1:
            st.markdown("### 📈 Maximum Similarity Trend")
            
            dates = [datetime.fromisoformat(entry['timestamp']) for entry in st.session_state.analysis_history]
            max_similarities = [entry['max_similarity'] for entry in st.session_state.analysis_history]
            
            fig_trends, ax_trends = plt.subplots(figsize=(10, 6))
            
            sns.lineplot(x=dates, y=max_similarities, marker='o', linewidth=2, markersize=8, color='#667eea')
            
            ax_trends.set_title("Maximum Similarity Trend Over Time", fontsize=16, fontweight='bold')
            ax_trends.set_xlabel("Date", fontsize=12)
            ax_trends.set_ylabel("Maximum Similarity (%)", fontsize=12)
            ax_trends.grid(True, alpha=0.3)
            
            if len(dates) > 1:
                z = np.polyfit(range(len(dates)), max_similarities, 1)
                p = np.poly1d(z)
                ax_trends.plot(dates, p(range(len(dates))), "--", alpha=0.8, color='red', label='Trend')
                ax_trends.legend()
            
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            st.pyplot(fig_trends)
        
        if st.button("🗑️ Clear History"):
            st.session_state.analysis_history = []
            st.rerun()
    else:
        st.info("No analysis history available. Run your first detection to see history here.")

with tab4:
    st.markdown("### ℹ️ Help & Documentation")
    
    st.markdown("""
    <div class="info-message">
        <h3>🎯 How to Use CADS</h3>
        <p>Follow these simple steps to detect code plagiarism:</p>
    </div>
    """, unsafe_allow_html=True)
    
    steps = [
        {
            "step": 1,
            "title": "Upload Files",
            "description": "Upload 2 or more code files using the file uploader. All files must have the same extension."
        },
        {
            "step": 2,
            "title": "Run Detection",
            "description": "Click the 'Run Plagiarism Detection' button to start the analysis process."
        },
        {
            "step": 3,
            "title": "Review Results",
            "description": "Examine the detailed results, interactive visualizations, and download reports as needed."
        }
    ]
    
    for step in steps:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 1rem; border-radius: 10px; margin: 1rem 0;">
            <h4>Step {step['step']}: {step['title']}</h4>
            <p>{step['description']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("### 🔧 How It Works")
    
    st.markdown("""
    **Algorithm**: CADS uses advanced fingerprinting technology:
    - **K-gram Analysis**: Breaks code into overlapping sequences of tokens
    - **Winnowing Algorithm**: Reduces fingerprint set while maintaining accuracy
    - **Similarity Scoring**: Calculates percentage overlap between source files
    
    **Supported Formats**: Common source code files (py, c, cpp, java, js, txt, etc.)
    
    **Performance**: Optimized for fast analysis of codebases with efficient memory usage
    """)
    
    st.markdown("### ❓ Frequently Asked Questions")
    
    faqs = [
        {
            "Q": "What is a good similarity threshold?",
            "A": "Generally, similarities above 70% indicate potential plagiarism, 30-70% suggest shared patterns, and below 30% are usually coincidental."
        },
        {
            "Q": "How accurate is the detection?",
            "A": "The algorithm is highly accurate for detecting copied code while being robust against minor modifications and formatting changes."
        },
        {
            "Q": "Can I analyze large codebases?",
            "A": "Yes, the system is optimized for large-scale analysis with efficient memory usage and parallel processing capabilities."
        }
    ]
    
    for faq in faqs:
        with st.expander(f"Q: {faq['Q']}"):
            st.write(f"A: {faq['A']}")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem; color: #666;">
    <p>CADS: Code Authenticity Detection System</p>
    <p>Developed with ❤️ by <b>Team Code Explorers</b></p>
</div>
""", unsafe_allow_html=True)

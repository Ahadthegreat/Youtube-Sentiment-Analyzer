# 📊 YouTube Comment Sentiment Analysis  

## 🌟 Why This Project?  
In today's digital age, YouTube is one of the biggest platforms for content consumption. Creators and businesses rely on user feedback to understand audience perception. However, manually analyzing thousands of comments is time-consuming and inefficient.  

This project **automates sentiment analysis** on YouTube comments, helping creators, marketers, and analysts understand the **audience's emotional response** towards a video—whether it's **positive, negative, or neutral**.  

---

## 🔍 How It Works  
The project follows a **systematic** approach to fetch, clean, analyze, and visualize YouTube comments:  

### 1️⃣ Fetch Comments  
- Uses **YouTube Data API v3** to fetch comments from a given video.  
- Filters out comments from the **uploader** to ensure unbiased sentiment analysis.  

### 2️⃣ Data Cleaning & Preprocessing  
- Removes **spammy links**, special characters, and **excessive emojis** using **Regex**.  
- Ensures only meaningful comments are analyzed.  

### 3️⃣ Sentiment Analysis  
- Uses **VADER Sentiment Analysis** to determine the polarity of each comment.  
- Classifies comments as **Positive, Negative, or Neutral** based on their sentiment score.  

### 4️⃣ Results & Insights  
- Stores filtered comments in a text file.  
- Displays the **most positive and most negative comments**.  
- Visualizes sentiment distribution using a **bar chart**.  

---

## 📌 Features  
✅ **Automated Comment Extraction** – Fetches comments directly from YouTube.  
✅ **Natural Language Processing (NLP)** – Uses VADER to classify sentiments.  
✅ **Spam & Irrelevant Content Filtering** – Removes links and excessive emojis.  
✅ **Fast & Efficient** – Optimized with **difference array technique** for quick processing.  
✅ **Data Visualization** – Generates a **bar chart** for sentiment analysis insights.  

---

## 🛠️ Technologies Used  
- **Python** 🐍  
- **YouTube Data API v3** 📺  
- **VADER Sentiment Analysis** 🧠  
- **Matplotlib** 📊  
- **Regular Expressions (Regex)** 🔎  

---

## 🚀 Getting Started  

### 🔧 Prerequisites  
- Python installed (`>=3.7`)  
- API Key for YouTube Data API v3  

### 📥 Installation  
1. Clone the repository:  
   ```bash
   git clone https://github.com/yourusername/youtube-comment-analysis.git
   cd youtube-comment-analysis

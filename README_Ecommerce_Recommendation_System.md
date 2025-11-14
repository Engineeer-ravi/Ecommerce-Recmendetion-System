
# 🛒 E-Commerce Recommendation System using Machine Learning & Flask

## 📘 Overview
This project is an **E-Commerce Recommendation System** built using **Machine Learning** and **Flask Web Framework**.  
It recommends similar products to users based on product descriptions, brands, and categories — just like how Amazon or Flipkart show “You may also like” or “Similar Products”.

The backend uses **TF-IDF Vectorization** and **Cosine Similarity** to find similar products, while the web interface is created using **HTML, CSS, and JavaScript** for a smooth user experience.

---

## 🚀 Features
- 📦 Recommends top 10 similar products based on product features.
- 💬 Uses TF-IDF and Cosine Similarity for accurate recommendations.
- 🧠 Supports both **content-based** and **user-based** recommendation logic.
- 🌐 Flask-based web app with a clean frontend (HTML, CSS, JS).
- 📊 Dataset preprocessed using **SpaCy NLP** for better text cleaning.
- 🔥 Simple UI for entering a product name and viewing recommendations.

---

## 🧰 Tech Stack
**Languages & Frameworks:**
- Python (Flask, Scikit-learn, Pandas, Numpy)
- HTML, CSS, JavaScript (Frontend)
- SpaCy (Text Cleaning and NLP)

**Libraries Used:**
```
pandas
numpy
scikit-learn
flask
spacy
matplotlib
seaborn
```
---

## 🗂️ Project Structure
```
E-Commerce Recomendation System/
│
├── app.py                               # Flask backend file
├── E-commerece Product Recommendatio.ipynb   # Machine Learning model notebook
├── static/                              # CSS, JS, Images (frontend assets)
├── templates/                           # HTML templates (index.html, result.html)
├── .venv/                               # Virtual environment
├── README.md                            # Project documentation
└── requirements.txt                     # Python dependencies (optional)
```

---

## 📊 Dataset Description
The dataset used is from **Walmart’s e-commerce product catalog**.  
It contains information such as:
- Product ID & Unique ID
- Product Name, Brand, Category
- Product Description
- Ratings and Review Count
- Image URL

**Example columns:**
```
['Uniq Id', 'Product Id', 'Product Name', 'Product Brand',
 'Product Category', 'Product Description', 'Product Rating', 
 'Product Reviews Count', 'Product Image Url']
```

---

## ⚙️ How It Works
1. Dataset is preprocessed (missing values filled, duplicates removed).
2. Product text data (category, brand, description) combined into a **Tags** column.
3. **SpaCy NLP** cleans the tags by removing stopwords and punctuation.
4. **TF-IDF Vectorizer** converts text into numeric features.
5. **Cosine Similarity** calculates similarity between products.
6. `recommend()` function retrieves top 10 most similar products.
7. Flask app displays results dynamically on the web interface.

---

## 🧠 Machine Learning Algorithm
**TF-IDF (Term Frequency–Inverse Document Frequency):**
- Converts textual data into numerical representation.

**Cosine Similarity:**
- Measures how similar two products are (based on vector angles).

Formula:  
```
similarity(A,B) = (A ⋅ B) / (||A|| * ||B||)
```

---

## 💻 Installation & Setup

### Step 1: Clone the Repository
```bash
git clone https://github.com/<your-username>/ecommerce-recommendation-system.git
cd ecommerce-recommendation-system
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate      # For Windows
source venv/bin/activate    # For Mac/Linux
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run Flask App
```bash
python app.py
```
Then open browser and visit → `http://127.0.0.1:5000/`

---

## 🖼️ Screenshots (Add yours here)
| Home Page | Recommendations Page |
|------------|----------------------|
| ![Home Page](static/homepage.png) | ![Results Page](static/results.png) |

---

## 🔮 Future Enhancements
- Integrate **Deep Learning (BERT)** for semantic similarity.
- Add **real-time user behavior tracking**.
- Implement **hybrid model (content + collaborative filtering)**.
- Deploy on **Render / AWS / Heroku** for live access.

---

## 👨‍💻 Author
**Ravi Pathak**  
🎓 Engineering Student | 💻 Machine Learning & Flask Developer  
📧 Email: patharavi.er@gmaill.com  
🌐 LinkedIn: [Your LinkedIn Profile](https://www.linkedin.com)

---

## ⭐ Acknowledgements
- Walmart Product Dataset
- SpaCy NLP
- Scikit-learn Documentation
- Flask Framework

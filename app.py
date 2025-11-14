from flask import Flask, render_template, request
import pandas as pd
import random
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import OperationalError
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)


# ============================================================
#  Load CSV files safely
# ============================================================
try:
    trending_products = pd.read_csv("models/trending_products.csv")
    train_data = pd.read_csv("models/clean_data.csv")
except FileNotFoundError as e:
    print(f"⚠ CSV File not found: {e}")
    trending_products = pd.DataFrame()
    train_data = pd.DataFrame()

# ============================================================
#  Database Configuration
# ============================================================
app.secret_key = "alskdjfwoeieiurlskdjfslkdjf"

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:@localhost:3307/ecom"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_POOL_RECYCLE'] = 280
app.config['SQLALCHEMY_POOL_TIMEOUT'] = 20
app.config['SQLALCHEMY_POOL_SIZE'] = 10
app.config['SQLALCHEMY_MAX_OVERFLOW'] = 5

db = SQLAlchemy(app)

# ============================================================
#  Database Models
# ============================================================
class Signup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)

class Signin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)

# ============================================================
#  Helper Functions
# ============================================================
def truncate(text, length):
    return text[:length] + "..." if len(text) > length else text

def content_based_recommendations(train_data, item_name, top_n=10):
    if train_data.empty or 'Name' not in train_data.columns or 'Tags' not in train_data.columns:
        print("⚠ Invalid or empty train_data file")
        return pd.DataFrame()

    if item_name not in train_data['Name'].values:
        print(f"Item '{item_name}' not found in training data.")
        return pd.DataFrame()

    tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix_content = tfidf_vectorizer.fit_transform(train_data['Tags'])
    cosine_similarities_content = cosine_similarity(tfidf_matrix_content, tfidf_matrix_content)

    item_index = train_data[train_data['Name'] == item_name].index[0]
    similar_items = list(enumerate(cosine_similarities_content[item_index]))
    similar_items = sorted(similar_items, key=lambda x: x[1], reverse=True)
    top_similar_items = similar_items[1:top_n+1]
    recommended_item_indices = [x[0] for x in top_similar_items]

    recommended_items_details = train_data.iloc[recommended_item_indices][
        ['Name', 'ReviewCount', 'Brand', 'ImageURL', 'Rating']
    ]
    return recommended_items_details

# ============================================================
#  Data for Homepage
# ============================================================
random_image_urls = [
    "static/img_1.png",
    "static/img_2.png",
    "static/img/img_3.png",
    "static/img_4.png",
    "static/img_5.png",
    "static/img_6.png",
    "static/img_7.png",
    "static/img_8.png",
]

prices = [40, 50, 60, 70, 100, 122, 106, 50, 30, 200, 150]

def prepare_index_data():
    num_products = 8
    products_to_show = trending_products.head(num_products)
    random_product_image_urls = [random.choice(random_image_urls) for _ in range(len(products_to_show))]
    random_price = random.choice(prices)

    return {
        'trending_products': products_to_show,
        'truncate': truncate,
        'random_product_image_urls': random_product_image_urls,
        'random_price': random_price
    }

# ============================================================
#  Routes
# ============================================================
@app.route('/')
def index():
    data = prepare_index_data()
    return render_template('index.html', **data)

@app.route('/main')
def main():
    # ✅ Pass an empty list to prevent UndefinedError in template
    return render_template('main.html', content_based_rec=[], message=None)

@app.route('/index')
def indexredirect():
    data = prepare_index_data()
    return render_template('index.html', **data)

# ============================================================
#  Signup
# ============================================================
@app.route("/signup", methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        try:
            new_signup = Signup(username=username, email=email, password=password)
            db.session.add(new_signup)
            db.session.commit()
            msg = "User signed up successfully! ✅"
        except OperationalError as e:
            print(f"Database Error: {e}")
            db.session.rollback()
            msg = "⚠ Database connection lost! Please try again."
        except Exception as e:
            print(f"Unexpected Error: {e}")
            db.session.rollback()
            msg = "⚠ Something went wrong."
        finally:
            db.session.close()

        random_product_image_urls = [random.choice(random_image_urls) for _ in range(len(trending_products))]
        random_price = random.choice(prices)
        return render_template('index.html',
                               trending_products=trending_products.head(8),
                               truncate=truncate,
                               random_product_image_urls=random_product_image_urls,
                               random_price=random_price,
                               signup_message=msg)
    else:
        return render_template('signup.html')

# ============================================================
#  Signin
# ============================================================
@app.route('/signin', methods=['POST', 'GET'])
def signin():
    if request.method == 'POST':
        username = request.form['signinUsername']
        password = request.form['signinPassword']

        new_signin = Signin(username=username, password=password)
        db.session.add(new_signin)
        db.session.commit()

        random_product_image_urls = [random.choice(random_image_urls) for _ in range(len(trending_products))]
        price = [40, 50, 60, 70, 100, 122, 106, 50, 30, 50]
        return render_template('index.html', 
                               trending_products=trending_products.head(8),
                               truncate=truncate,
                               random_product_image_urls=random_product_image_urls,
                               random_price=random.choice(price),
                               signup_message='User signed in successfully!')

    return render_template('signin.html')

# ============================================================
#  Recommendations
# ============================================================
@app.route("/recommendations", methods=['POST', 'GET'])
def recommendations():
    if request.method == 'POST':
        prod = request.form.get('prod')
        nbr = int(request.form.get('nbr', 5))
        content_based_rec = content_based_recommendations(train_data, prod, top_n=nbr)

        if content_based_rec.empty:
            message = "No recommendations available for this product."
            return render_template('main.html', content_based_rec=[], message=message)

        random_product_image_urls = [random.choice(random_image_urls) for _ in range(len(content_based_rec))]
        random_price = random.choice(prices)
        return render_template('main.html', 
                               content_based_rec=content_based_rec,
                               truncate=truncate,
                               random_product_image_urls=random_product_image_urls,
                               random_price=random_price,
                               message=None)
    else:
        return render_template('main.html', content_based_rec=[], message=None)

# ============================================================
#  Run App
# ============================================================
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

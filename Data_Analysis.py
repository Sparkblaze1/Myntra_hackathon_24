import pandas as pd
import plotly.express as px
import nltk
from collections import Counter
from nltk.corpus import stopwords
import re
nltk.download('punkt')
nltk.download('stopwords')
data = pd.read_csv('clothing_prompts_1000.csv')
colors = ["red", "blue", "green", "yellow", "purple", "pink", "black", "white", "grey", "orange", "gold", "silver"]
styles = [
    "evening gown", "summer dress", "business suit", "tracksuit", "maxi dress", "A-line dress", "knitted sweater",
    "gothic-style dress", "denim jacket", "saree", "beachwear outfit", "winter coat", "jumpsuit", "steampunk-themed outfit",
    "casual outfit", "lehenga", "kurta", "bridal lehenga", "sherwani", "anarkali suit"
]
details = [
    "sequins", "floral patterns", "fitted blazer", "hoodie", "tiered layers", "polka dots",
    "turtleneck", "lace details", "white t-shirt", "intricate embroidery", "sarong wrap",
    "faux fur lining", "metallic fabric", "corset", "graphic t-shirt", "heavy embroidery",
    "intricate patterns", "elaborate designs", "gold embroidery", "flowing fabric"
]
additional_details = [
    "featuring a V-neck", "short sleeves", "pencil skirt", "matching joggers", "off-shoulder neckline", "cinched waist",
    "long sleeves", "high neckline", "skinny jeans", "matching blouse", "colorful bikini",
    "sleek lin

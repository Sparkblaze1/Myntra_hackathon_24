import streamlit as st
from openai import OpenAI
import requests
from PIL import Image
from io import BytesIO
import pandas as pd
from geopy.distance import geodesic
import random
import geocoder

api_key = "sk-proj-7ZRLrlCZtcvQRmhvmH77T3BlbkFJWgroXKO98L4MXUlf9me1" # OPEN-AI API key - DALL-e 3 version used
client = OpenAI(api_key=api_key)

def display_app():
    
    bg_color = "#0A135E"
    page_bg_img = f'''
  <style>
    body {{
      background-color: {bg_color};
    }}
  </style>
  '''
    st.markdown(page_bg_img, unsafe_allow_html=True)

display_app()

def display_page1():
    st.image('C://Users/admin/PycharmProjects/myntra_hackathon/src/header.png')
    st.header('_AI-Powered customized dress designer_ ⭐', divider='rainbow')

    # Get user input
    user_description = st.text_area("Enter the description of the custom dress : ")

    if st.button("Generate Image"):
        if not user_description:
            st.error("Please enter a description.")
        else:
            with st.spinner("Generating image..."):
                try:
                    # Constructing promts based on user's needs
                    prompt = (
                        f"Generate a realistic image of a custom dress based on the following description: {user_description}. "
                        "The dress should be shown in a full view, displaying both the front side clearly. "
                        "Use realistic textures, shadows, and lighting to make the dress appear lifelike. "
                        "The dress should be worn by a model standing in a pretty background but highlight the dress design more. "
                        "Include fine details of the fabric, stitching, and design elements to make the dress look high-quality and desirable. As realistic as possible."
                    )

                    # Image generation
                    response = client.images.generate(
                        model="dall-e-3",
                        prompt=prompt,
                        size="1024x1024",
                        quality="standard",
                        n=1,
                    )

                    # URL of the image obtained
                    image_url = response.data[0].url

                    # Display image
                    response = requests.get(image_url)
                    img = Image.open(BytesIO(response.content))
                    st.image(img, caption="Generated Dress Image", use_column_width=True)

                except Exception as e:
                    st.error(f"An error occurred: {e}")

    if st.button("View Similar designs", key="page1_button"):
        st.session_state["page"] = "page2" 


def display_page2():
    st.image('C://Users/admin/PycharmProjects/myntra_hackathon/src/header.png')

    def generate_random_locations(center_location, max_distance, seed):
        random.seed(seed)
        locations = []
        for _ in range(10):
            latitude_offset = random.uniform(-max_distance, max_distance)
            longitude_offset = random.uniform(-max_distance, max_distance)

            new_latitude = center_location[0] + latitude_offset
            new_longitude = center_location[1] + longitude_offset

            locations.append((new_latitude, new_longitude))
        return locations

    def generate_random_names(num_names, seed):
        random.seed(seed)
        boutique_names = [
            'Chic Boutique', 'Elegant Attire', 'Fashion Forward', 'Trendy Threads', 'Style Haven',
            'Glamour House', 'Couture Corner', 'Boutique Bliss', 'Vogue Vault', 'Fashion Fiesta'
        ]
        if num_names > len(boutique_names):
            raise ValueError("Number of names requested exceeds available unique names.")
        return random.sample(boutique_names, k=num_names)

    def generate_star_rating(rating):
        full_stars = int(rating)
        half_star = 1 if rating % 1 >= 0.5 else 0
        return '⭐' * full_stars + '✰' * half_star

    def get_current_location():
        try:
            g = geocoder.ip('me')
            current_location = g.latlng
            return current_location
        except Exception as e:
            print(f"Error getting location: {e}")
            return None

    current_location = get_current_location()

    max_distance = 0.1
    seed = 42

    random_locations = generate_random_locations(current_location, max_distance, seed)
    random.seed(seed)
    ratings = [round(random.uniform(3.5, 5.0), 1) for _ in range(10)]
    names = generate_random_names(10, seed)
    imgs = [
        "https://via.placeholder.com/150",
        "https://via.placeholder.com/150",
        "https://via.placeholder.com/150",
        "https://via.placeholder.com/150",
        "https://via.placeholder.com/150",
        "https://via.placeholder.com/150",
        "https://via.placeholder.com/150",
        "https://via.placeholder.com/150",
        "https://via.placeholder.com/150",
        "https://via.placeholder.com/150",
    ]

    data = {
        'name': names,
        'latitude': [loc[0] for loc in random_locations],
        'longitude': [loc[1] for loc in random_locations],
        'rating': ratings,
        'image': imgs
    }
    boutiques = pd.DataFrame(data)
    boutiques['distance'] = boutiques.apply(
        lambda row: geodesic(current_location, (row['latitude'], row['longitude'])).km, axis=1)
    nearby_boutiques = boutiques.sort_values(by=['distance', 'rating'], ascending=[True, False])

    st.markdown(
        """
        <style>
        .main {
            background-color: #001f3f;
            color: white;
        }
        .stImage img {
            border-radius: 10px;
        }
        .stTitle, .stSubtitle, .stMarkdown {
            color: white;
        }
        hr {
            border: 1px solid #FF5733;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.title("Nearby Boutiques Finder")
    st.map(boutiques[['latitude', 'longitude']])

    st.subheader("Boutiques List")
    cols = st.columns(4)
    for i, (index, row) in enumerate(nearby_boutiques.iterrows()):
        col = cols[i % 4]
        with col:
            st.image(row['image'], width=150)
            st.markdown(f"<h4 style='color: #FF5733;'>{row['name']}</h4>", unsafe_allow_html=True)
            st.markdown(f"<p style='color: #FF5733;'>📍 Distance: {row['distance']:.2f} km</p>", unsafe_allow_html=True)
            st.markdown(f"<p style='color: #FF5733;'>{generate_star_rating(row['rating'])}</p>", unsafe_allow_html=True)
            st.markdown("<hr>", unsafe_allow_html=True)

page = st.session_state.get("page", "page1") 

if page == "page1":
    display_page1()
elif page == "page2":
    display_page2()

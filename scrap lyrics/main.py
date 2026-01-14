import requests
import re
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS

# -------------------------------
# Step 1: Fetch Lyrics
# -------------------------------
def get_lyrics(artist, song):
    url = f"https://api.lyrics.ovh/v1/{artist}/{song}"
    response = requests.get(url)

    print("Status Code:", response.status_code)

    if response.status_code == 200:
        data = response.json()
        return data.get("lyrics", "")
    else:
        return ""

# -------------------------------
# Step 2: Clean Lyrics
# -------------------------------
def clean_text(text):
    text = text.lower()
    text = re.sub(r"\[.*?\]", "", text)   # remove [chorus], [verse]
    text = re.sub(r"[^a-z\s]", "", text)  # remove special characters
    return text

# -------------------------------
# Step 3: Word Cloud
# -------------------------------
def generate_wordcloud(text):
    stopwords = set(STOPWORDS)

    wordcloud = WordCloud(
        width=800,
        height=400,
        background_color="black",
        stopwords=stopwords,
        colormap="plasma"
    ).generate(text)

    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()

# -------------------------------
# MAIN PROGRAM
# -------------------------------
print("Example to test:")
print("Artist: ed sheeran")
print("Song: perfect\n")

artist = input("Enter Artist Name: ").strip()
song = input("Enter Song Name: ").strip()

lyrics = get_lyrics(artist, song)

# Fallback (VERY IMPORTANT)
if not lyrics:
    print("Lyrics not found! Using demo lyrics.")
    lyrics = """
    I found a love for me
    Darling just dive right in and follow my lead
    Well I found a girl beautiful and sweet
    """

clean_lyrics = clean_text(lyrics)
generate_wordcloud(clean_lyrics)

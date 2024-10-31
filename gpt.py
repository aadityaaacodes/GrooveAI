from openai import OpenAI
import openai
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path='keys.env')
openai.api_key = f"{os.getenv('gpt_api')}"


def send_prompt(li):
    prompt = f'''
    Using this list of songs and artists, {li}:
    Produce a new list of at least 15 songs by recommended artists from a diverse range of countries and languages who embody the same emotional resonance, tonal texture, and atmospheric vibe as [the original artist]? I’m particularly interested in musicians who reflect a similar balance of melodic progression, harmonic layering, and vocal timbre. The goal is to identify artists who approach production with a comparable sensitivity to soundscapes, maintaining the original artist's depth of sound and stylistic integrity. Please include recommendations for specific songs and album names that best represent each artist, highlighting tracks that most strongly reflect their style in relation to the original artist’s work. I’d appreciate details such as the album from which the song originates, the playlist where the track may be featured, the song’s duration in milliseconds, and an indication of whether it contains explicit content. These selections should capture the core essence of each artist’s sound and align with the original artist's musical qualities. Additionally, I would love recommendations that incorporate diverse regional musical elements—whether in instrumentation, vocal techniques, or rhythmic phrasing—and that showcase how these artists share similar branding or thematic elements with the original artist. Look for artists with strong visual identities, thematic consistency, or innovative marketing approaches that parallel the original artist’s brand. By broadening the scope to include both musical and branding aspects, along with specific songs and album names, I hope to discover a rich variety of global sounds that enhance the emotional impact while preserving the central tone, pacing, and overall ‘feel’ of the music. 
    Output new List in the format: [["song", "artist", "Explicit(or NE)", "duration"], [], []]. 
    Dont write anything else(even an introduction or any other irrelevant titles, subtitles, etc)
    '''
    completion = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"user", "content":f"{prompt}"}]
    )
    return(completion.choices[0].message.content)





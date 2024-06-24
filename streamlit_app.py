import streamlit as st
import pandas as pd
import requests
import altair as alt

##create first columns for title and image
col1, col2 = st.columns([3,1])

with col1:
    st.title('Pokemon Explorer!')

with col2:
    st.image('https://github.com/Charlie-martinzzz/Pokeball/blob/main/Pokemon-Pokeball.png?raw=true')


## create slider to select pokemon
pokemon_number = st.slider("Choose your Pokemon!", 1 , 151)

## get data
pokemon_url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_number}"
response = requests.get(pokemon_url).json()

pokemon_name = response['name'].capitalize()
pokemon_height = response['height'] * 10
total_moves = len(response['moves'])
pokemon_weight = response['weight'] / 10
image_url = response['sprites']['front_default']
moves = [move['move']['name'].capitalize() for move in response['moves']]
sound = response['cries']['latest']

## create next columns for info and image
col3, col4 = st.columns([3,2])

## display pokemon name and info
with col3:
    st.title(f"{pokemon_name} !")
    st.write(f"{pokemon_name} is {pokemon_height}cm tall and weighs {pokemon_weight} kg!")
    st.write(f"{pokemon_name} has {total_moves} potential moves!")

## show pokemon image
with col4:
    st.markdown(f'<img src="{image_url}" style="max-width: 300px; width: 100%; height: auto;">', unsafe_allow_html=True)



## create selectbox to show all pokemon moves
moves_list = st.selectbox("Select a move!" , moves)

st.write("How does your pokemon sound?")
st.audio(sound)

st.header("Compare your Pokemon!")
st.write("Click on the buttons below to add your pokemon to a chart")


# Initialize height comparison list in session state
if 'height_comparison_list' not in st.session_state:
    st.session_state.height_comparison_list = []

# Initialize weight comparison list in session state
if 'weight_comparison_list' not in st.session_state:
    st.session_state.weight_comparison_list = []


## create columns for buttons
col5, col6 = st.columns([2,1])

## button for height
with col5:
    if st.button("Add to height comparison"):
        st.session_state.height_comparison_list.append((pokemon_name, pokemon_height))
    
    # Reset height comparison 
    if st.button("Reset height comparison"):
        st.session_state.height_comparison_list = []

## button for weight
with col6:
    if st.button("Add to weight comparison"):
        st.session_state.weight_comparison_list.append((pokemon_name, pokemon_weight))   

    # Reset weight comparison 
    if st.button("Reset weight comparison"):
        st.session_state.weight_comparison_list = []

## add white space for readability
st.write("")
st.write("")

# Display height in a bar chart
if st.session_state.height_comparison_list:
    height_comparison_df = pd.DataFrame(st.session_state.height_comparison_list, columns=['Name', 'Height'])
    chart1 = alt.Chart(height_comparison_df).mark_bar().encode(
        x='Name',
        y=alt.Y('Height', axis=alt.Axis(title='Height (cm)')),  
    ).properties(
        title='Pokemon Height Comparison',  
        width=600,
        height=400
    )
    st.altair_chart(chart1)

# Display weight in a bar chart
if st.session_state.weight_comparison_list:
    weight_comparison_df = pd.DataFrame(st.session_state.weight_comparison_list, columns=['Name', 'Weight'])
    chart2 = alt.Chart(weight_comparison_df).mark_bar().encode(
        x='Name',
        y=alt.Y('Weight', axis=alt.Axis(title='Weight (kg)')),
    ).properties(
        title='Pokemon Weight Comparison',  
        width=600,
        height=400
    )
    st.altair_chart(chart2)


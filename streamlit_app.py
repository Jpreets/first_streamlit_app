import streamlit;
import pandas;
import requests;
import snowflake.connector;
from urllib.error import URLError

streamlit.title("My Parents New Healthy Diner");

streamlit.header("🥣 Breakfast Menu");
streamlit.text("🥗 Omega 3 & Blueberry Oatmeal");
streamlit.text("🐔 Kale, Spinach & Rocket Smoothie");
streamlit.text("🥑🍞 Hard Boiled Free-Range Eggs");

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt");

my_fruit_list = my_fruit_list.set_index('Fruit');

fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),["Avocado","Strawberries"]);
fruits_to_show = my_fruit_list.loc[fruits_selected];

streamlit.dataframe(fruits_to_show);

streamlit.header("Fruityvice Fruit Advice!");



def get_fruityvice_data(this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+this_fruit_choice);
    # write your own comment -what does the next line do? 
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json());
    return fruityvice_normalized;

try:
    fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
    if not fruit_choice:
          streamlit.error('Please enter Fruit to get info')
    else:    
        fruityvice_normalized = get_fruityvice_data(fruit_choice);
        streamlit.dataframe(fruityvice_normalized);


    

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
my_data_row = my_cur.fetchone()
streamlit.text("Hello from Snowflake:")
streamlit.text(my_data_row)


def get_fruit_load_list():
    with  my_cnx.cursor() as my_cur
    my_cur.execute("SELECT * from fruit_load_list ")
    return my_cur.fetchall();
    
def insert_row_snowflake(new_fruit):
    with  my_cnx.cursor() as my_cur
    my_cur.execute("insert into fruit_load_list values('"+new_fruit+"')");
    return 'Thanks for Adding new Fruit '+new_fruit;

if streamlit.button('Get Fruit List'):
    my_data_rows = get_fruit_load_list();
    streamlit.header("Fruit load list contain:")
    streamlit.dataframe(my_data_rows);    

add_my_fruit = streamlit.text_input('What fruit would you like to add');
if streamlit.button('Add Fruit to the List'):
    message = insert_row_snowflake(add_my_fruit);
    streamlit.text(message);    

except URLError as e:
   streamlit.error();

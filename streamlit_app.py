# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col 

# Write directly to the app
st.title(":cup_with_straw: Customize your Smoothie :cup_with_straw: ")
st.write(
    """Choose the fruits you want in your smoothie!
    """
)


name_on_order = st.text_input("Name of Smoothie:", "")
st.write("The name of your smoothie will be:", name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()
fruit_dataframe = (session
                .table("smoothies.public.fruit_options")
                .select(col("FRUIT_NAME"))
               )
# st.dataframe(data=fruit_dataframe, use_container_width=True)

ingredient_list = st.multiselect(
    "Choose up to five ingedients",
    fruit_dataframe,
    max_selections = 5
)

if ingredient_list:
    ingredients_string = ""

    for fruit_chosen in ingredient_list:
        ingredients_string += fruit_chosen + ' '
    
    st.write( ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
                values ('""" + ingredients_string + """'
                        ,'""" + name_on_order + """')"""
    # st.write( my_insert_stmt)

    time_to_insert = st.button("Submit Order")

    succes_string = 'Your Smoothie is ordered, ' + name_on_order + '!'
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(succes_string, icon="✅")

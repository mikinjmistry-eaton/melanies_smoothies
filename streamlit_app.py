# Import python packages
import streamlit as st
import requests
from snowflake.snowpark.functions import col



# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie!"""
)

cnx = st.connection("snowflake")
session = cnx.session()

name_on_order = st.text_input('Name on Smoothie:')

st.write('The name on your Smoothie will be:', name_on_order)

my_dataframe = session.table("smoothies.public.fruit_options")
ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    my_dataframe.select("FRUIT_NAME").to_pandas()["FRUIT_NAME"].tolist(),
)
if ingredients_list:
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '


    my_insert_stmt = """insert into smoothies.public.orders(ingredients, name_on_order) values ('""" + ingredients_string + """', '""" + name_on_order + """')"""

    time_to_insert = st.button("Submit Order")

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")

# smoothiefroot_response = requests.get(
#     "https://my.smoothiefroot.com/api/fruit/watermelon"
# )

# sf_df = st.dataframe(
#     data=smoothiefroot_response.json(),
#     use_container_width=True
# )


if ingredients_list:

    for fruit_chosen in ingredients_list:

        st.subheader(fruit_chosen + ' Nutrition Information')

        search_on = session.table("SMOOTHIES.PUBLIC.FRUIT_OPTIONS") \
            .filter(col("FRUIT_NAME") == fruit_chosen) \
            .select(col("SEARCH_ON")) \
            .collect()[0][0]

        smoothiefroot_response = requests.get(
            "https://my.smoothiefroot.com/api/fruit/" + search_on
        )

        st.dataframe(
            data=smoothiefroot_response.json(),
            use_container_width=True
        )

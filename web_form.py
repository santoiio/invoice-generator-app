import streamlit as st
import pandas as pd
from pdf_gen import pdf_gen

df1 = pd.read_csv("hustles.csv")

st.header("Invoice generator")
with st.form("invoice_data"):
    st.subheader("Customer Info")
    st.write(r"*No need to capitalize anything.")
    customer_info = {
        "company" : st.text_input("Company", placeholder="e.g. Acme LLC"),
        "name" : st.text_input("Name", placeholder="Enter the customer's "
                                                   "full name"),
        "address" : st.text_input("Address", placeholder="e.g. 123 Main St."),
        "city_st_zip" : st.text_input("City, St, Zip", placeholder="e.g. "
                                                        "Dallas, Tx, 75214"),
        "email" : st.text_input("Email", placeholder="e.g. "
                                                     "something@email.com"),
        "note" : st.text_input("Additional Notes", placeholder="e.g. An "
                            "additional fee will be charged at this date"),
        "business" : st.selectbox("Which business is this for?",
                                       df1["hustle"])
    }
    st.markdown("---")
    st.subheader("Invoice Items")


    products = []
    col1, col2, col3 = st.columns([3, 1, 1])
    for i in range(1,7):
        with col1:
            product_name = st.text_input("Product Name", key=f"pn{i}")

        with col2:
            qty = st.number_input("Quantity", key=f"q{i}", step=1)

        with col3:
            unit_price = st.number_input("Price", key=f"up{i}")
        # Only add filled in products
        if product_name:
            products.append({
                "product_name": product_name,
                "unit_price": unit_price,
                "qty": qty,
                "total": unit_price * qty,
            })


    button = st.form_submit_button("Generate Invoice")

if button:
    if products:
        # Calculate subtotal
        subtotal = sum(item["total"] for item in products)

        # Add customer details ONLY to the first row
        for index, product in enumerate(products):
            if index == 0:
                product.update(customer_info)
                product["sub_total"] = subtotal
            else:
                product.update({key: "" for key in customer_info.keys()})
                product["sub_total"] = ""

        # Create DataFrame and save as CSV
        df = pd.DataFrame(products)
        filename = "invoices/invoice_data.csv"
        df.to_csv(filename, index=False)

        st.success("Your invoice has been emailed to the customer and a copy "
                   "should be in your inbox.")

        pdf_gen()

    else:
        st.warning("You need to enter at least one product to generate the "
                   "invoice")



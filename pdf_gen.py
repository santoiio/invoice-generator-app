import glob, tempfile, time
from fpdf import FPDF
import pandas as pd
from pathlib import Path
import streamlit as st
from send_email import send_email
from get_image import header_image, thanks_image


def pdf_gen():
    filepaths = glob.glob("invoices/invoice_data.csv")

    for filepath in filepaths:

        # Generate a PDF
        pdf = FPDF(orientation="P", unit="mm", format="A4")
        pdf.set_left_margin(20)
        pdf.set_right_margin(20)
        pdf.add_page()
        df = pd.read_csv(filepath)

        # Name the invoice
        for index, row in df.iterrows():
            phrase = str(row["business"])
            id = ''.join(word[0].upper() for word in phrase.split())
            break
        filename = f"{id}-10{time.strftime('%m%H')}"
        invoice_nr = filename
        date = time.strftime("%b %d, %Y")

        # Add header background according to business
        header_image(pdf, id)

        # Add invoice number headers
        pdf.set_y(40)
        pdf.set_font(family="Helvetica", size=36, style="B")
        pdf.cell(w=50, h=8, txt="INVOICE")
        pdf.set_font(family="Helvetica", size=16, style="B")
        pdf.set_text_color(50,50,50)
        pdf.cell(w=120, h=4, txt=f"NO: {invoice_nr}", align="R", ln=1)
        pdf.ln(16)

        # Add "bill to" and "from"
        pdf.set_font(family="Helvetica", size=20, style="B")
        pdf.cell(w=50, h=8, txt="Bill To:")
        pdf.cell(w=120, h=8, txt="From:", align="R", ln=1)


        info=[]
        for index, row in df.iterrows():
            pdf.set_font(family="Helvetica", size=16)
            pdf.set_text_color(80, 80, 80)

            # Check if 'company' is NaN, if so replace with an empty string
            company = str(row["company"]).title() if pd.notna(row["company"]) \
                else ""
            info.append(company)
            name = str(row["name"]).title() if pd.notna(row["name"]) else ""
            info.append(name)
            address = str(row["address"]).title() if pd.notna(row["address"]) \
                else ""
            info.append(address)
            city_st_zip = str(row["city_st_zip"]).title() if pd.notna(
                row["city_st_zip"]) else ""
            info.append(city_st_zip)
            email = str(row["email"]) if pd.notna(row["email"]) else ""
            info.append(email)

        # Add Billing info
        pdf.set_left_margin(22)
        pdf.set_text_color(80,80,80)
        pdf.cell(w=100, h=8, txt=info[0])
        pdf.cell(w=67, h=8, txt="Maximiliano Santoyo", align="R", ln=1)
        pdf.cell(w=120, h=8, txt=info[1])
        pdf.cell(w=47, h=8, txt="830-309-1564", align="R", ln=1)
        pdf.cell(w=120, h=8, txt=info[2], ln=1)
        pdf.cell(w=120, h=8, txt=info[3], ln=1)
        pdf.cell(w=120, h=8, txt=info[4])

        pdf.set_left_margin(20)
        pdf.ln(8)
        pdf.cell(w=50, h=20, txt=f"Date: {date}", ln=1)

        # Add a chart and column headers
        columns = df.columns
        columns = [item.replace("_", " ").title() for item in columns]
        pdf.set_font(family="Helvetica", size=10, style="B")

        #Adjust header colors according to business
        if id == "CL":
            pdf.set_fill_color(1,73,38)
        elif id == "ID":
            pdf.set_fill_color(96,67,45)
        elif id == "MPR":
            pdf.set_fill_color(69,109,184)
        else:
            pdf.set_fill_color(20, 28, 131)

        pdf.set_text_color(255,255,255)
        pdf.cell(w=80, h=8, txt=columns[0], border=0, align="C", fill=True)
        pdf.cell(w=20, h=8, txt=columns[1], border=0, align="C", fill=True)
        pdf.cell(w=35, h=8, txt=columns[2], border=0, align="C", fill=True)
        pdf.cell(w=35, h=8, txt=columns[3], border=0, align="C", fill=True,
                 ln=1)

        # Add rows to the table with product information
        product_count = 0
        for index, row in df.iterrows():
            product_name = str(row["product_name"]) if pd.notna(
                row["product_name"]) else ""
            qty = str(row["qty"]) if pd.notna(
                row["qty"]) else ""
            unit_price = str(row["unit_price"]) if pd.notna(
                row["unit_price"]) else ""
            total = str(row["total"]) if row["total"] != 0 else ""
            pdf.set_font(family="Helvetica", size=10)
            pdf.set_text_color(80,80,80)
            pdf.cell(w=80, h=8, txt=product_name, border=1)
            pdf.cell(w=20, h=8, txt=qty, align="C", border=1)
            pdf.cell(w=35, h=8, txt=unit_price, align="C", border=1)
            pdf.cell(w=35, h=8, txt=total, align="C", border=1, ln=1)

            product_count += 1

        for i in range(6 - product_count):
            pdf.cell(w=80, h=8, txt="", border=1)
            pdf.cell(w=20, h=8, txt="", border=1)
            pdf.cell(w=35, h=8, txt="", border=1)
            pdf.cell(w=35, h=8, txt="", border=1, ln=1)
        pdf.ln(6)

        # Calculate and add Sub Total below chart
        total_sum = df["sub_total"].sum()
        if id == "CL":
            pdf.set_fill_color(1, 73, 38)
        elif id == "ID":
            pdf.set_fill_color(96, 67, 45)
        elif id == "MPR":
            pdf.set_fill_color(60, 162, 122)
        else:
            pdf.set_fill_color(20, 28, 131)

        pdf.set_text_color(255, 255, 255)
        pdf.cell(w=100, h=8, txt="", border=0)
        pdf.cell(w=35, h=8, txt="Sub Total", border=0, align="C", fill=True)
        pdf.cell(w=35, h=8, txt=f"$ {str(total_sum)}", border=0, align="C",
                 fill=True, ln=1)
        pdf.ln(8)

        # Add Notes
        pdf.set_text_color(80, 80, 80)
        pdf.set_font(family="Helvetica", size=14, style="B")
        pdf.cell(w=15, h=8, txt="Note:")
        x = pdf.get_x()
        y = pdf.get_y()
        pdf.line(x,y + 6, x + 70, y + 6)
        pdf.line(x-14,y + 14, x + 70, y + 14)

        for index, row in df.iterrows():
            if index == 0:
                note = str(row["note"])[:68] if pd.notna(row["note"]) else ""

                pdf.set_font(family="Helvetica", size=14)
                pdf.set_x(20)
                pdf.multi_cell(w=84, h=8, txt=f"         {note}")
                pdf.ln(8)

        # Add payment info
        pdf.set_font(family="Helvetica", size=20, style="B")
        pdf.set_text_color(50,50,50)
        pdf.cell(w=50, h=8, txt="Payment Information:", ln=1)
        pdf.set_font(family="Helvetica", size=14, style="B")
        pdf.cell(w=15, h=8, txt="Zelle:")
        pdf.set_font(family="Helvetica", size=14)
        pdf.cell(w=15, h=8, txt="830-309-1564", ln=1)
        pdf.set_font(family="Helvetica", size=10, style="B")

        # Add thank you according to business
        thanks_image(pdf, id, x, y)
        pdf.ln(12)

        # Add warranty information
        pdf.set_text_color(0, 0, 0)
        if id == "CL":
            pdf.multi_cell(w=95, h=6, txt=r"Contractor warranty includes unglued "
                r"lights and clips. *Not liable for damage from tampering"
                r" or natural forces ")
        else:
            pdf.multi_cell(w=95, h=6, txt=r"*Contractor is not liable for "
                                    r"any injuries from handling equipment")

        # Generate a temporary file
        with tempfile.NamedTemporaryFile(delete=False,
                                         suffix=".pdf") as temp_pdf:
            temp_path = temp_pdf.name  # Store the temporary path
            pdf.output(temp_path)  # Save the PDF file

        # Define a user-friendly filename
        custom_filename = f"{filename}.pdf"
        final_attachment_path = Path(
            temp_path).parent / custom_filename  # Store in the same directory

        # Rename the temp file to a meaningful name
        Path(temp_path).rename(final_attachment_path)

        # Email the PDF with a proper filename
        attachment_path = str(final_attachment_path)
        message = f"""Please find attached the invoice #{invoice_nr}.
Let me know if you have any questions.

Payment can be made via Zelle to 830-309-1564.

Thank you for your business!

Best regards,  
Maximiliano Santoyo
        """
        subject = f"{phrase} Invoice #{invoice_nr} - Payment Details Attached"
        receivers = [info[4], st.secrets["u_name1"]]
        send_email(subject, receivers, message, attachment_path)

        # Clean up: Delete the temp file after sending the email
        Path(final_attachment_path).unlink()

if __name__ == "__main__":
    pdf_gen()
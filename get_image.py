import requests
from fpdf import FPDF
from pathlib import Path


def header_image(pdf, id):
    image_url = (
                f"https://raw.githubusercontent.com/santoiio/invoice-generator"
                f"-app/main/images/{id.lower()}.jpg")
    image = "header.jpg"
    response = requests.get(image_url)

    if response.status_code == 200:
        with open(image, "wb") as file:
            file.write(response.content)
        print(f"Image {image} downloaded successfully.")
        # Ensure the file was written before using it
        if Path(image).exists():
            return pdf.image(image, x=0, y=0, w=210)
        else:
            print("Error: Image file not found after download.")
    else:
        print(
            f"Error: Failed to download image. Status code {response.status_code}")


def thanks_image(pdf, id, x, y):
    image_url = (
                f"https://raw.githubusercontent.com/santoiio/invoice-generator"
                f"-app/main/images/{id.lower()}_tky.jpg")
    image = "thanks.jpg"
    response = requests.get(image_url)

    if response.status_code == 200:
        with open(image, "wb") as file:
            file.write(response.content)
        print(f"Image {image} downloaded successfully.")
        # Ensure the file was written before using it
        if Path(image).exists():
            return pdf.image(image, x=x + 90, y=y, w=60)
        else:
            print("Error: Image file not found after download.")
    else:
        print(
            f"Error: Failed to download image. Status code {response.status_code}")
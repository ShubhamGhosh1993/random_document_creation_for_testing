from django.http import HttpResponse,JsonResponse
import random
import requests
from io import BytesIO
import threading
import os
from reportlab.pdfgen import canvas
from lorem_text import lorem
from reportlab.lib.pagesizes import A4
from reportlab.platypus import Image
from faker import Faker
import shutil
import zipfile
from django.http import HttpResponse
from django.views import View

def pdfCreation(pageNo):
    folder_name='output'
    image_folder_name = 'image'
    output_path=f"{folder_name}/{lorem.words(1)}.pdf"
    image_path=f"{image_folder_name}/{lorem.words(1)}.jpg"

    #Check the folder exists
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    if not os.path.exists(image_folder_name):
        os.makedirs(image_folder_name)

    # Create a canvas (PDF)
    c = canvas.Canvas(output_path, pagesize=A4)
    for j in range(pageNo):
        lines = random.randint(15, 100)
        if j == 0 :
            fake=Faker()
            image_url = fake.image_url()
            response_image = requests.get(image_url)
            print(image_url)
            image_data = BytesIO(response_image.content)
            image_file = open(image_path, "+wb")
            image_file.write(image_data.read())
            image_file.close()
            # Add the image to the PDF
            c.drawImage(image_path, 5, 5,width=550,height=750)
        else:
            for i in range(lines):
                no_of_words = random.randint(5, 15)
                # Set font and draw the page number
                c.setFont('Helvetica', 12)
                c.drawString(3, 800-i*10, lorem.words(no_of_words))
        c.showPage()        
    # Save the canvas (PDF)  
    c.save()

def hello_world(req):
    return JsonResponse({'message': 'Hello, world!'})

def downloadPdf(req, num):
    threads = []
    for i in range(num):  
        pageNo = random.randint(2, 10)    
        th=threading.Thread(target=pdfCreation, args=[pageNo])
        threads.append(th)
        th.start()

    for thread in threads:
        thread.join()

    # Define the path to the folder you want to zip
    folder_path = 'output'
    # Create a temporary directory to store the zip file
    temp_dir = 'pdfDoc'
    os.makedirs(temp_dir, exist_ok=True)
    # Create a temporary zip file
    temp_zipfile = os.path.join(temp_dir, 'output.zip')
    # Zip the folder contents
    with zipfile.ZipFile(temp_zipfile, 'w') as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, folder_path)
                zipf.write(file_path, arcname=arcname)
    # Open the zip file
    with open(temp_zipfile, 'rb') as f:
        response = HttpResponse(f.read(), content_type='application/zip')
        response['Content-Disposition'] = f'attachment; filename={temp_dir}.zip'
    # Delete the temporary files and directory
    # os.remove(temp_zipfile)
    # os.rmdir(temp_dir)
    # os.rmdir("output")
    # os.rmdir("image")
    shutil.rmtree(temp_dir)
    shutil.rmtree("output")
    shutil.rmtree("image")

    return response
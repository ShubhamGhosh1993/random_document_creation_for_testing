# importing all the required dependencies
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
from ebooklib import epub


# Set the output folders
folder_name='output'
image_folder_name = 'image'
epub_folder_name='epub_output'
epub_image_folder_name = 'epub_image'

# delete the folders after creation
def deleteFolders():
    #remove folder_name
    if os.path.exists(folder_name):
        shutil.rmtree(folder_name)

    #remove image_folder_name
    if os.path.exists(image_folder_name):
        shutil.rmtree(image_folder_name)

    #remove epub_older_name
    if os.path.exists(epub_folder_name):
        shutil.rmtree(epub_folder_name)

    #remove epub_image_folder_name
    if os.path.exists(epub_image_folder_name):
        shutil.rmtree(epub_image_folder_name)

    return
# create the pdf files
def pdfCreation(pageNo):
    output_path=f"{folder_name}/{lorem.words(1)}.pdf"
    image_path=f"{image_folder_name}/{lorem.words(1)}.jpg"

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

#download-pdf route hits this function for getting the pdfs generated 
def downloadPdf(req, num):
    #Check the folder exists
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    if not os.path.exists(image_folder_name):
        os.makedirs(image_folder_name)

    threads = []
    for i in range(num):  
        pageNo = random.randint(2, 10)    
        th=threading.Thread(target=pdfCreation, args=[pageNo])
        threads.append(th)
        th.start()

    for thread in threads:
        thread.join()

    # Define the path to the folder you want to zip
    folder_path = folder_name
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
    shutil.rmtree(temp_dir)
    deleteFolders()

    return response

# create the epub files
def epubCreation(pageNo):
    # Create a new EPUB book
    book = epub.EpubBook()
    # Set metadata
    book.set_identifier(lorem.words(1))
    book.set_title(lorem.words(4))
    book.set_language('en')
    
    # Add an author
    book.add_author(lorem.words(2))

    for i in range(1, pageNo+1):
        page_title=f'Chapter {i}'
        content = f'<h1>Chapter {i} Content</h1><p>{lorem.paragraphs(2)}</p>'
        # Create a page
        page=epub.EpubHtml(title=page_title, file_name=f'chapter_{i}.xhtml', content=content)
        book.add_item(page)
        book.add_item(epub.EpubNcx())
        book.spine.append(page)

    # Add the table of contents to the book
    book.add_item(epub.EpubNav())
    
    # Create the EPUB file
    epub.write_epub(f'{epub_folder_name}/{lorem.words(1)}.epub', book)

# download-epub route hits this function for getting the pdfs generated 
def downloadEpub(req,num):
    #Check the folder exists
    if not os.path.exists(epub_folder_name):
        os.makedirs(epub_folder_name)
    if not os.path.exists(epub_image_folder_name):
        os.makedirs(epub_image_folder_name)

    #threads array that contents each thread
    threads = []
    # looping through the threads
    for i in range(num):  
        pageNo = random.randint(2, 10)    
        th=threading.Thread(target=epubCreation, args=[pageNo])
        threads.append(th)
        th.start()

    for thread in threads:
        thread.join()

    # Define the path to the folder you want to zip
    folder_path = epub_folder_name
    # Create a temporary directory to store the zip file
    temp_dir = 'epubDoc'
    os.makedirs(temp_dir, exist_ok=True)
    # Create a temporary zip file
    temp_zipfile = os.path.join(temp_dir, f'{temp_dir}.zip')
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
    shutil.rmtree(temp_dir)
    deleteFolders()
    
    return response


# api/generate_html.py
import xml.etree.ElementTree as ET
import os

def generate_html_from_xml(xml_file, output_html_file):
    # Parse the XML file
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Start building the HTML content
    html_content = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>RSS Feed Data</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f4f4f4; }
            header { background: #007BFF; color: #fff; padding: 10px 20px; text-align: center; }
            h1 { margin: 0; }
            .container { max-width: 800px; margin: 20px auto; padding: 20px; background: #fff; border-radius: 8px; box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1); }
            .feed-item { margin-bottom: 20px; padding: 15px; border: 1px solid #ddd; border-radius: 5px; background: #f9f9f9; }
            .feed-item img { max-width: 100%; height: auto; border-radius: 5px; }
            .feed-item h2 { margin: 0 0 10px; font-size: 1.5em; }
            .feed-item a { text-decoration: none; color: #007BFF; }
            .feed-item a:hover { text-decoration: underline; }
            footer { text-align: center; margin-top: 20px; font-size: 0.9em; color: #666; }
        </style>
    </head>
    <body>
        <header>
            <h1>RSS Feed Data</h1>
        </header>
        <div class="container">
    '''

    # Iterate through each item in the XML and add to HTML
    for item in root.findall('.//item'):
        title = item.find('title').text if item.find('title') is not None else "No Title"
        link = item.find('link').text if item.find('link') is not None else "#"
        image = item

import os
import time
import subprocess
import requests
import xml.etree.ElementTree as ET

def fetch_rss_feeds(rss_urls):
    feed_data = []
    for url in rss_urls:
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an error for bad responses
            print(f"Fetched data from {url}")

            # Parse the XML response
            root = ET.fromstring(response.content)
            items = root.findall('.//item')  # Adjust based on the XML structure

            if not items:
                print(f"No items found in the feed from {url}")

            for item in items:
                title = item.find('title').text if item.find('title') is not None else "No Title"
                link = item.find('link').text if item.find('link') is not None else "#"
                image = item.find('{http://search.yahoo.com/mrss/}content').attrib['url'] if item.find('{http://search.yahoo.com/mrss/}content') is not None else "No URL"
                
                feed_data.append({
                    'title': title,
                    'link': link,
                    'image': image
                })
        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch RSS feed from {url}: {e}")

    # Create XML from feed_data
    feeds = ET.Element('feeds', version='1.0')
    items_element = ET.SubElement(feeds, 'items')

    for feed in feed_data:
        item_element = ET.SubElement(items_element, 'item')
        ET.SubElement(item_element, 'title').text = feed['title']
        ET.SubElement(item_element, 'link').text = feed['link']
        ET.SubElement(item_element, 'image').text = feed['image']

    # Save XML to a file
    with open('rssFeedData.xml', 'w', encoding='utf-8') as f:
        f.write(ET.tostring(feeds, encoding='unicode'))

    print("XML file 'rssFeedData.xml' generated successfully.")

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
        image = item.find('image').text if item.find('image') is not None else None

        html_content += f'''
        <div class="feed-item">
            <h2><a href="{link}" target="_blank">{title}</a></h2>
            {f'<img src="{image}" alt="{title}">' if image else '<p>No Image Available</p>'}
        </div>
        '''

    # Close the HTML tags
    html_content += '''
        </div>
        <footer>
            <p>Generated by RSS Feed Fetcher</p>
        </footer>
    </body>
    </html>
    '''

    # Write the HTML content to a file
    with open(output_html_file, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"HTML file '{output_html_file}' generated successfully.")

def main():
    rss_urls = [
        "https://bankless.com/rss/feed",
        "https://checkpoint.cc/rss/updates"
    ]
    
    # Fetch RSS feeds and generate XML
    fetch_rss_feeds(rss_urls)
    
    # Generate HTML from the XML
    generate_html_from_xml('rssFeedData.xml', 'rssFeedData.html')

if __name__ == "__main__":
    while True:
        main()
        print("Waiting for the next update...")
        time.sleep(86400)  # Sleep for 86400 seconds (1440 minutes)


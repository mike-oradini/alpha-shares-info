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
    # Open the file in write mode ('w') to overwrite any existing data
    with open('rssFeedData.xml', 'w', encoding='utf-8') as f:
        f.write(ET.tostring(feeds, encoding='unicode'))

    print("XML file 'rssFeedData.xml' generated successfully.")

# Example RSS Feed URLs (Replace these with your specific feeds)
rss_urls = [
    "https://bankless.com/rss/feed",
    "https://checkpoint.cc/rss/updates"
]

# Fetch and store feeds
fetch_rss_feeds(rss_urls)

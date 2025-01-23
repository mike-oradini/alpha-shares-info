// RSS Feed Fetcher
// Fetches and stores titles, links, and image URLs from RSS feeds into a JSON object
const fetch = require('node-fetch'); // Add this line
const fs = require('fs'); // Add this line

const fetchRSSFeeds = async (rssUrls) => {
    const feedData = [];

    for (const url of rssUrls) {
        try {
            const response = await fetch(url);
            const text = await response.text();
            const parser = new DOMParser();
            const xml = parser.parseFromString(text, "text/xml");

            const items = xml.querySelectorAll("item");

            items.forEach(item => {
                const title = item.querySelector("title") ? item.querySelector("title").textContent : "No Title";                
                const link = item.querySelector("link") ? item.textContent || "#" : "Links";
                const image = item.querySelector("media\\:content") ? item.getAttribute("url") : "No URL"; // Fixed this line
                feedData.push({
                    title: title,
                    link: link,
                    image: image
                });
            });
        } catch (error) {
            console.error(`Failed to fetch RSS feed from ${url}:`, error);
        }
    }

    // Save feedData to a JSON file
    fs.writeFileSync("rssFeedData.json", JSON.stringify(feedData)); // Updated this line

    return feedData;
};

// Example RSS Feed URLs (Replace these with AlphaShares-specific feeds)
const rssUrls = [
    "https://bankless.com/rss/feed"
];

// Fetch and store feeds
fetchRSSFeeds(rssUrls).then(data => console.log("RSS Feed Data Fetched:", data)).catch(error => console.error(error)); // Added catch for unhandled promise rejection

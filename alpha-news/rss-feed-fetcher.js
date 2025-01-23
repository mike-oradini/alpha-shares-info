// RSS Feed Fetcher
// Fetches and stores titles, links, and image URLs from RSS feeds into a JSON object
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
                const title = item.querySelector("title")?.textContent || "No Title";
                const link = item.querySelector("link")?.textContent || "#";
                const image = item.querySelector("media\\:content")?.getAttribute("url") || 
                              item.querySelector("enclosure")?.getAttribute("url") || "default-image.jpg";

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

    // Save feedData to local storage or a JSON file
    localStorage.setItem("rssFeedData", JSON.stringify(feedData));

    return feedData;
};

// Example RSS Feed URLs (Replace these with AlphaShares-specific feeds)
const rssUrls = [
    "https://alphashares.io/rss-feed-1.xml",
    "https://alphashares.io/rss-feed-2.xml"
];

// Fetch and store feeds
fetchRSSFeeds(rssUrls).then(data => console.log("RSS Feed Data Fetched:", data));

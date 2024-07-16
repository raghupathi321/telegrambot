import requests
from bs4 import BeautifulSoup
import json
import telebot
from datetime import datetime

# Replace with your Telegram bot token
TELEGRAM_BOT_TOKEN = "7284623018:AAF56exVB7FbjmTcOKsKojySvFuieu9JotA"
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# List of URLs to scrape
URLS = [
    "https://www.blackhatworld.com/",
    "https://pastebin.com/",
    "https://gist.github.com/",
    "https://news.ycombinator.com/",
    "https://www.reddit.com/",
]


def scrape_data(urls, limit=20):
    results = []

    for url in urls:
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.content, "html.parser")

            # Example: Scraping titles or specific content
            titles = soup.find_all("h2")[:limit]  # Limiting to 20 pairs

            for title in titles:
                result = {
                    "Source": url,
                    "Content": title.text.strip(),
                    "Type": "Data leak",
                    "Detection Date": datetime.now().strftime("%d %b %Y %H:%M:%S"),
                    "Detection Link": response.url,
                }
                results.append(result)

        except Exception as e:
            print(f"Error scraping {url}: {str(e)}")

    return results


@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.reply_to(message, "Welcome! Send /scan to initiate data scraping.")


@bot.message_handler(commands=["scan"])
def scan_data(message):
    results = scrape_data(URLS, limit=20)

    if results:
        formatted_results = []
        for result in results:
            formatted_result = f"Source: {result['Source']}\nContent: {result['Content']}\nType: {result['Type']}\nDetection Date: {result['Detection Date']}\nDetection Link: {result['Detection Link']}\n\n"
            if len(formatted_result) <= 4096:  # Check Telegram message length limit
                formatted_results.append(formatted_result)

        if formatted_results:
            for msg in formatted_results:
                bot.send_message(message.chat.id, msg)
        else:
            bot.send_message(message.chat.id, "No data scraped.")
    else:
        bot.send_message(message.chat.id, "No data scraped.")


if __name__ == "__main__":
    bot.polling()

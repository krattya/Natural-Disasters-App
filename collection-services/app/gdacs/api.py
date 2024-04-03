import feedparser


def _get_data_from_api():
    # Fetch the RSS feed from GDACS
    gdacs_feed = feedparser.parse("https://www.gdacs.org/xml/rss.xml")

    # Extract events from the RSS feed
    events = gdacs_feed.entries
    # print(events)
    # gdac_events = [GdacEvent(**event) for event in events]
    # print(gdac_events[0].title)
    return events


def get_all_alerts():
    return _get_data_from_api()

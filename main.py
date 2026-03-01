from data_fetch import EbayDataFetcher

if __name__ == "__main__":
    fetcher = EbayDataFetcher()

    results = fetcher.search_active_listings(
        keyword="Levi 501",
        limit=10
    )

    for item in results:
        print(item)
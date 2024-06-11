from googlesearch import search
from keywords import get_keywords_from_url, check_nltk_data



check_nltk_data()


data = dict()

def main():
	query = "used car"
	for result in search(query, 10):
			print(f"Processing URL: {result}")
			try:
				keywords = get_keywords_from_url(result)
				for k, v in keywords.items():
					data[k] = data.get(k, 0) + v
				# break
			except Exception as e:
				print(f"Error processing URL {result}: {e}")
	print(sorted(data.items(), key=lambda item: item[1], reverse=True))

if __name__ == "__main__":
    main()


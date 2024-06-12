from googlesearch import search
from requests.exceptions import ReadTimeout, HTTPError, ConnectionError
from keywords import format_ngrams, get_keywords_from_url, check_nltk_data 
import time

check_nltk_data()

freq_dicts_total = [dict(), dict(), dict()]


def format_freq_dict(freq_d, n=20):
    sorted_freq_d = sorted(freq_d.items(), key=lambda item: item[1], reverse=True)
    return sorted_freq_d[:n]

def main():
    query = "used car"
    for result in search(query, 200):
        print(f"Processing URL: {result}")
        try:
            time.sleep(0.3)
            freq_dicts = get_keywords_from_url(result)

            # keywords = get_keywords_from_url(result)
            for i, freq_dict in enumerate(freq_dicts):
                 for k, v in freq_dict.items():
                    freq_dicts_total[i][k] = freq_dicts_total[i].get(k, 0) + v
        except Exception as e:
            # print(f"Error processing URL {result}: {e}")
            pass
    print("Top 20 Single Words:")
    print(format_freq_dict(freq_dicts_total[0]))
    print("\nTop 20 Bigrams:")
    print(format_freq_dict(freq_dicts_total[1]))
    print("\nTop 20 Trigrams:")
    print(format_freq_dict(freq_dicts_total[2]))

if __name__ == "__main__":
    main()


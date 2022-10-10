# from duckduckgo_search import ddg

# keywords = 'google'
# results = ddg(keywords, region='wt-wt', safesearch='Moderate', time='y', max_results=1000000)  # 1 milion
# for result in results:
#     print(result)

from serpapi import GoogleSearch
search = GoogleSearch({"q": "coffee", "location": "Austin,Texas", "api_key": "secretKey"})
result = search.get_dict()

print(result)
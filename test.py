from googlesearch import search
# https://stackoverflow.com/questions/38635419/searching-in-google-with-python
results = search('"google"', num_results=10000)
# print(len(list(results)))
print(type(results))

# for results in results:
#     print(result)
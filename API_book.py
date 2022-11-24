import requests

r = requests.get('http://localhost:8000/book/api/books/')

print(r.json())
print(r.status_code)

r = requests.post('http://localhost:8000/book/api/books/', data={
    'name':'Книга из приложения Python',
    "price":"293.92"}
                  )

print(r.json())
print(r.status_code)


r = requests.get('http://localhost:8000/book/api/books/19')

print(r.json())
print(r.status_code)

# r = requests.put('http://localhost:8000/book/api/books/19', data={
#     'name':'Книга из приложения Python',
#     "price":"293.92"}
#                   )
#
# print(r.json())
# print(r.status_code)


r = requests.delete('http://localhost:8000/book/api/books/19')

print(r.status_code)

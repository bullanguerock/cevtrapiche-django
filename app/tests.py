DJANGO_ALLOWED_CORS =http://127.0.0.1:8080 https://127.0.0.1:8080 [::1]

cors = [(DJANGO_ALLOWED_CORS.split(' '))]

print('cors')


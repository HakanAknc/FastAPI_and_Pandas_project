# FastAPI_and_Pandas_project

# Kullanım
Bu örnek uygulama, birkaç temel HTTP yönlendiricisini içermektedir:

GET /: Temel bir "hello world" yanıtı döner.
POST /: Bir POST isteğine yanıt olarak "hello from the post route" döner.
PUT /: Bir PUT isteğine yanıt olarak "hello from the put route" döner.
GET /users: "list users route" mesajını döner.
GET /users/me: "this is the current user" mesajını döner.
GET /users/{user_id}: Belirtilen kullanıcı kimliğiyle ilgili bilgileri döner.
Ayrıca, özel bir FoodEnum türü kullanarak farklı yiyecekleri temsil eden özel bir yol (GET /foods/{food_name}) ve daha fazlasını içerir.

# Katkı
Eğer bu projeye katkıda bulunmak isterseniz, lütfen bir çekme isteği (pull request) göndermekten çekinmeyin!

# FastAPI Example Application
This is an example application created using FastAPI. FastAPI is used to create RESTful APIs in Python, known for its modern and fast approach.

# Usage
This example application includes several basic HTTP routers:

GET /: Returns a basic "hello world" response.
POST /: Returns "hello from the post route" in response to a POST request.
PUT /: Returns "hello from the put route" in response to a PUT request.
GET /users: Returns the "list users route" message.
GET /users/me: Returns the "this is the current user" message.
GET /users/{user_id}: Returns information related to the specified user ID.
It also includes a custom route (GET /foods/{food_name}) that represents different foods using a custom FoodEnum type and much more.

# Contributions
If you'd like to contribute to this project, feel free to submit a pull request!

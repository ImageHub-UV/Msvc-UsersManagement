from django.test import TestCase, Client
from rest_framework.test import APIClient
from .models import User

class Utils():
    def create_user(self, client, email, first_name, last_name, username, password):
        return client.post('/auth/users/', {
            "email":email,
            "first_name":first_name,
            "last_name":last_name,
            "username":username,
            "password":password,
            "re_password":password,
        })
                    

class TestUserMsvc(TestCase):
    def setUpTestData():
        c = Client()
        utils = Utils()

        

        response = utils.create_user(c, "samueltrujillo85@yopmail.com", "Samuel", "Trujillo", "SamuelTrujillo10", "MandeSamuel2023")  
        utils.create_user(c, "manuelgalindo85@yopmail.com", "Manuel", "Galindo", "ManuelGalindo10", "MandeManuel2023")
        utils.create_user(c, "saralopez85@yopmail.com", "Sara", "Lopez", "SaraLopez10", "MandeSara2023")
        utils.create_user(c, "santiagopaz85@yopmail.com", "Santiago", "Paz", "SantiagoPaz10", "MandeSantiago2023")
        utils.create_user(c, "mariavargas85@yopmail.com", "Maria", "Vargas", "MariaVargas10", "MandeMaria2023")

        size = User.objects.all().count()

        assert response.status_code == 201
        assert size == 5

    def test_get_users(self):
        c = Client()
        response = c.get('/user/get/1')

        assert response.status_code == 200
        assert response.data['email'] == "samueltrujillo85@yopmail.com"
        assert response.data['first_name'] == "Samuel"
        assert response.data['last_name'] == "Trujillo"
        assert response.data['username'] == "SamuelTrujillo10"

        response = c.get('/user/get/3')

        assert response.status_code == 200
        assert response.data['email'] == "saralopez85@yopmail.com"
        assert response.data['first_name'] == "Sara"
        assert response.data['last_name'] == "Lopez"
        assert response.data['username'] == "SaraLopez10"
        


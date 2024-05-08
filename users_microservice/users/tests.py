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
    
    def active_user(self, id):
        user = User.objects.get(id=id)
        user.is_active = True
        user.save()

    def get_token(self, client, username, password):
        return client.post('/auth/jwt/create/', {
            "username":username,
            "password":password
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

        utils.active_user(1)
        utils.active_user(2)
        utils.active_user(3)
        
        size = User.objects.all().count()
        
        assert response.status_code == 201
        assert size == 5
        assert User.objects.get(id=1).is_active == True

    def test_get_users(self):
        c = Client()
        response = c.get('/user/do/1')

        assert response.status_code == 200
        assert response.data['email'] == "samueltrujillo85@yopmail.com"
        assert response.data['first_name'] == "Samuel"
        assert response.data['last_name'] == "Trujillo"
        assert response.data['username'] == "SamuelTrujillo10"

        response = c.get('/user/do/3')

        assert response.status_code == 200
        assert response.data['email'] == "saralopez85@yopmail.com"
        assert response.data['first_name'] == "Sara"
        assert response.data['last_name'] == "Lopez"
        assert response.data['username'] == "SaraLopez10"

    def test_get_user_not_found(self):
        c = Client()
        response = c.get('/user/do/10')
        assert response.status_code == 404

    def test_delete_user(self):
        c = Client()
        
        response = c.delete('/user/do/1')
        assert response.status_code == 200

        u1 = User.objects.get(id=1)
        assert not u1.is_active

    def test_delete_user_not_active(self):
        c = Client()
        response = c.delete('/user/do/4')
        assert response.status_code == 400

    def test_delete_user_not_found(self):
        c = Client()
        response = c.delete('/user/do/10')
        assert response.status_code == 404
        
    def test_get_token(self):
        c = Client()
        utils = Utils()
        
        response = utils.get_token(c, "SamuelTrujillo10", "MandeSamuel2023")
        assert response.status_code == 200
        assert 'access' in response.data
        assert 'refresh' in response.data

    def test_get_token_user_not_found(self):
        c = Client()
        utils = Utils()
        
        response = utils.get_token(c, "SamuelTrujillo11", "MandeSamuel2023")
        assert response.status_code == 401

    def test_get_token_wrong_password(self):
        c = Client()
        utils = Utils()
        
        response = utils.get_token(c, "SamuelTrujillo10", "MandeSamuel2024")
        assert response.status_code == 401

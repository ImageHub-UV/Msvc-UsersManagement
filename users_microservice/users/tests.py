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

    def test_get_token_inactive_user(self):
        c = Client()
        utils = Utils()
        
        response = utils.get_token(c, "MariaVargas10", "MandeMaria2023")
        content = response.content.decode('utf-8')

        assert response.status_code == 401
        assert 'No active account found with the given credentials' in content

    def test_verify_token(self):
        c = APIClient()
        utils = Utils()

        token = utils.get_token(c, "SamuelTrujillo10", "MandeSamuel2023")
        c.credentials(HTTP_AUTHORIZATION='JWT ' + token.data['access'])

        response = c.post('/auth/jwt/verify/', {'token':token.data['access']})
        assert response.status_code == 200

    def test_verify_token_wrong_token(self):
        c = APIClient()
        utils = Utils()

        token = utils.get_token(c, "SamuelTrujillo10", "MandeSamuel2023")

        response = c.post('/auth/jwt/verify/', {'token':token.data['access']+'1'})
        assert response.status_code == 401
    
    def test_verify_token_not_authenticated(self):
        c = APIClient()
        utils = Utils()

        response = c.post('/auth/jwt/verify/', {'token':'token'})
        assert response.status_code == 401

    def test_refresh_token(self):
        c = APIClient()
        utils = Utils()

        token = utils.get_token(c, "SamuelTrujillo10", "MandeSamuel2023")
        c.credentials(HTTP_AUTHORIZATION='JWT ' + token.data['access'])

        response = c.post('/auth/jwt/refresh/', {'refresh':token.data['refresh']})
        assert response.status_code == 200
        assert 'access' in response.data

    def test_user_modification(self):
        c = APIClient()
        utils = Utils()

        token = utils.get_token(c, "SamuelTrujillo10", "MandeSamuel2023")
        c.credentials(HTTP_AUTHORIZATION='JWT ' + token.data['access'])

        response = c.patch('/auth/users/me/', 
                           {'first_name':'Samuelito', 'last_name':'Trujillito'})

        u1 = User.objects.get(id=1)
        assert u1.first_name == 'Samuelito'
        assert u1.last_name == 'Trujillito'
            
    def test_user_modification_not_authenticated(self):
        c = APIClient()
        utils = Utils()

        response = c.patch('/auth/users/me/', 
                           {'first_name':'Samuelito', 'last_name':'Trujillito'})

        assert response.status_code == 401

    def test_user_modification_wrong_token(self):
        c = APIClient()
        utils = Utils()

        token = utils.get_token(c, "SamuelTrujillo10", "MandeSamuel2023")
        c.credentials(HTTP_AUTHORIZATION='JWT ' + token.data['access'] + '1')

        response = c.patch('/auth/users/me/', 
                           {'first_name':'Samuelito', 'last_name':'Trujillito'})

        assert response.status_code == 401

    def test_change_password(self):
        c = APIClient()
        utils = Utils()

        token = utils.get_token(c, "SamuelTrujillo10", "MandeSamuel2023")
        c.credentials(HTTP_AUTHORIZATION='JWT ' + token.data['access'])

        response = c.post('/auth/users/set_password/', 
                          {'new_password':'MandeSamuel2024', 're_new_password':'MandeSamuel2024', 'current_password':'MandeSamuel2023'})

        token = utils.get_token(c, "SamuelTrujillo10", "MandeSamuel2024")

        assert response.status_code == 204
        assert 'access' in token.data



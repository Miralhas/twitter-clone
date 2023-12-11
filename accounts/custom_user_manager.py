from django.contrib.auth.models import BaseUserManager
from django.utils import timezone

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        '''
        Cria e salva um usuário, com o email e senha passados no argumento.
        '''
        if not email:
            raise ValueError("Usuários precisam ter um email")
        
        now = timezone.now()
        email = self.normalize_email(email)
        
        # Quando um novo user for criado esses campos serão preenchidos automaticamente.
        # não vai precisar passar cada um deles no User.objects.create_user().
        # Apenas os necessários para autenticação: ...create_user(email, password)
        # Caso o seu User Model tenha novos campos eles serão pegos pelo **extra_fields.
        # User.objects.create_user(email, password, date_of_birth, phone_number)
        # date_of_birth e phone_number são colunas que vc adicionou no User(AbstractUser)
        user = self.model(
            email=email,
            is_staff=is_staff, 
            is_active=True,
            is_superuser=is_superuser, 
            last_login=now,
            date_joined=now, 
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        return self._create_user(email, password, False, False, **extra_fields)
    
    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True, **extra_fields)
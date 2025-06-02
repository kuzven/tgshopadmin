from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class BotUserManager(BaseUserManager):
    def create_user(self, telegram_id, first_name, username=None, last_name=None):
        if not telegram_id:
            raise ValueError("У пользователя должен быть Telegram ID")
        user = self.model(
            telegram_id=telegram_id,
            username=username,
            first_name=first_name,
            last_name=last_name
        )
        user.save(using=self._db)
        return user

class BotUser(AbstractBaseUser):
    telegram_id = models.PositiveIntegerField(unique=True, verbose_name="Telegram ID")
    username = models.CharField(max_length=255, blank=True, null=True, verbose_name="Имя пользователя")
    first_name = models.CharField(max_length=255, verbose_name="Имя")
    last_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="Фамилия")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата регистрации")

    password = None  # Отключаем пароль
    last_login = None  # Отключаем поле "Последний вход"

    objects = BotUserManager()

    USERNAME_FIELD = 'telegram_id'
    REQUIRED_FIELDS = ['first_name']

    def set_password(self, raw_password):
        pass  # Отключаем установку пароля

    def check_password(self, raw_password):
        return False  # Отключаем проверку пароля

    def __str__(self):
        return f"{self.first_name} ({self.telegram_id})"

    class Meta:
        verbose_name = "Пользователь бота"
        verbose_name_plural = "Пользователи бота"

class Mailing(models.Model):
    user = models.ForeignKey(BotUser, on_delete=models.CASCADE, verbose_name="Пользователь")
    subject = models.CharField(max_length=255, verbose_name="Тема сообщения")
    message = models.TextField(verbose_name="Текст сообщения")
    sent_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата отправки")

    def __str__(self):
        return f"Рассылка для {self.user.first_name} ({self.user.telegram_id}) - {self.subject}"

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"

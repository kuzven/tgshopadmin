# tgshopadmin
Django admin panel for telegram bot shop

## Описание  
Проект **tgshopadmin** — это административная панель Django для управления Telegram ботом tgshopbot.

---

## 🛠 Системные требования  
Перед установкой убедитесь, что на сервере **уже запущены контейнеры**:  
- **PostgreSQL** → [Инструкция по установке](https://github.com/kuzven/postgres)  
- **Nginx Proxy Manager** → [Инструкция по установке](https://github.com/kuzven/nginxproxymanager)

---

## Инструкция по установке и запуску на сервере с Docker

### **1️⃣ Клонирование репозитория**

```bash
cd ~
git clone https://github.com/kuzven/tgshopadmin.git
cd tgshopadmin
```

### **2️⃣ Создание .env файла**
- Создаём .env на основе шаблона:

```bash
cp .env.example .env
nano .env
```

- Сгенерируйте DJANGO_SECRET_KEY с помощью любого онлайн-генератора, например:

```
https://djecrety.ir/
```

- Скопируйте ключ и вставьте его в .env.
- Укажите значения для следующих параметров, например:

```
DJANGO_SECRET_KEY=n-v24$r$nmfhume8aeho@04nto(34$ir#_%4h1hx4xug&m71s7
DEBUG=0
ALLOWED_HOSTS=domain.com,www.domain.com,127.0.0.1,ip_address_vps
CSRF_TRUSTED_ORIGINS=http://domain.com,http://www.domain.com,http://127.0.0.1,http://ip_address_vps

PG_DATABASE=tgshop_db
PG_USER=tgshop_user
PG_PASSWORD=SecurePassword
PG_HOST=postgres
PG_PORT=5432

# Настройки статики
# На локальном ПК использовать True (чтобы загружать файлы из static/)
# На сервере (продакшн) использовать False (чтобы загружать файлы из STATIC_ROOT)
USE_STATICFILES_DIRS=False
```

### **3️⃣ Настройка nginx.conf**

```bash
nano nginx.conf
```

- Укажите реальные домены в строке:

```
server_name domain.com www.domain.com;
```

### **4️⃣ Подготовка базы данных PostgreSQL**
Создаём базу данных tgshop_db и пользователя tgshop_user с доступом.

```bash
docker exec -it postgres psql -U admin -c "CREATE DATABASE tgshop_db;"
docker exec -it postgres psql -U admin -c "CREATE USER tgshop_user WITH LOGIN PASSWORD 'SecurePassword';"
docker exec -it postgres psql -U admin -c "ALTER DATABASE tgshop_db OWNER TO tgshop_user;"
docker exec -it postgres psql -U admin -c "GRANT ALL PRIVILEGES ON DATABASE tgshop_db TO tgshop_user;"
```

### **5️⃣ Запуск контейнера с tgshopadmin**
Запускаем контейнеры tgshopadmin-web и tgshopadmin-nginx в фоне.

```bash
docker-compose up --build -d
```

### **6️⃣ Проверка запущенных контейнеров**

```bash
docker ps
```

Если weather-web и weather-nginx запущены, то переходим к настройке Django.

### **7️⃣ Применение миграций**

```bash
docker exec -it tgshopadmin-web python manage.py migrate
```

### **8️⃣ Создание суперпользователя**

```bash
docker exec -it tgshopadmin-web python manage.py createsuperuser --username admin --email admin@example.com
```

### **9️⃣ Сборка статических файлов**

```bash
docker exec -it tgshopadmin-web python manage.py collectstatic --noinput
```

### **🔟 Настройка Nginx Proxy Manager**

Создайте Proxy Hosts для проекта, в поле Domain Names укажите домен, в Scheme укажите http, в Forward Hostname / IP укажите weather-nginx, в Forward Port укажите 80. При необходимости можно создать SSL сертификат в разделе SSL Certificates.

Теперь проект tgshopadmin успешно запущен и должен быть доступен по указанному домену 🎉
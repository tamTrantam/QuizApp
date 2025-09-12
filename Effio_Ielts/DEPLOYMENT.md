# RENDER DEPLOYMENT GUIDE
# =======================

## Environment Variables to Set in Render Dashboard:

### Required Environment Variables:
```
DEBUG=False
SECRET_KEY=your-super-secret-key-here-make-it-long-and-random
ALLOWED_HOSTS=your-app-name.onrender.com
DATABASE_URL=postgresql://user:password@hostname:port/database
```

### Email Configuration (Optional - for production emails):
```
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-specific-password
```

### Security Settings (Production):
```
SECURE_SSL_REDIRECT=True
CSRF_COOKIE_SECURE=True
SESSION_COOKIE_SECURE=True
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_HSTS_PRELOAD=True
```

### AllAuth Settings:
```
ACCOUNT_EMAIL_VERIFICATION=mandatory
ACCOUNT_LOGIN_METHODS=email
ACCOUNT_UNIQUE_EMAIL=True
```

## Render Deployment Steps:

1. **Connect GitHub Repository**
   - Go to Render Dashboard
   - Click "New +" → "Web Service"
   - Connect your GitHub repository

2. **Configure Build Settings**
   - Build Command: `./build.sh`
   - Start Command: `gunicorn Effio_Ielts.wsgi:application`
   - Environment: `Python 3`

3. **Add Environment Variables**
   - Go to Environment tab
   - Add all the environment variables listed above
   - Make sure to generate a new SECRET_KEY for production

4. **Database Setup**
   - Add PostgreSQL database in Render
   - Copy the DATABASE_URL to environment variables

5. **Domain Configuration**
   - Add your custom domain (optional)
   - Update ALLOWED_HOSTS environment variable

## Local Development with Environment Variables:

1. **Create .env file** (copy from .env.example):
```bash
cp .env.example .env
```

2. **Edit .env file** with your local settings:
```
DEBUG=True
SECRET_KEY=your-local-secret-key
DATABASE_URL=postgresql://postgres:password@localhost:5432/effio_ielts_db
```

3. **Test locally**:
```bash
pipenv run python manage.py runserver
```

## Security Checklist:

- [ ] SECRET_KEY is different for production
- [ ] DEBUG=False in production
- [ ] Database credentials are secure
- [ ] ALLOWED_HOSTS is configured correctly
- [ ] SSL redirect is enabled for production
- [ ] Email backend is configured for production
- [ ] Static files are served via WhiteNoise

## Troubleshooting:

- **Static files not loading**: Check STATIC_ROOT and WhiteNoise configuration
- **Database connection issues**: Verify DATABASE_URL format
- **Email not working**: Check EMAIL_* environment variables
- **CSRF errors**: Ensure CSRF_COOKIE_SECURE matches your HTTPS setup
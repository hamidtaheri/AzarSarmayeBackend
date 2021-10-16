from settings import *

# make tests faster
# SOUTH_TESTS_MIGRATE = False
# DATABASES['default'] = {'ENGINE': 'django.db.backends.sqlite3'}
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': os.path.join(BASE_DIR, 'db_test.sqlite3'),
        'NAME': os.path.join(BASE_DIR, 'db_test.sqlite3'),
    }
}

print(f'DATABASES  {DATABASES}')

#
# 自動セットアップ用スクリプト
# SuperUserが存在しない場合に強制作成する
#

from django.contrib.auth import get_user_model
User = get_user_model()

if not User.objects.filter(is_active = True, is_staff = True, is_superuser = True).exists():
  username_base = 'admin'
  password = 'adminpassword'

  for i in range(1, 10):
    username = username_base + str(i)
    if not User.objects.filter(username = username).exists():
      print(f'Create supser user: {username}/{password}')
      User.objects.create_superuser(
        username, 'admin@example.test', password)
      
      break
  else:
    print("Error: Failed to create super user.")
    exit(1)


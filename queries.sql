SELECT "shop_app_product"."id", "shop_app_product"."category_id", "shop_app_product"."title", "shop_app_product"."description", "shop_app_product"."price", "shop_app_product"."image", "shop_app_product"."available" FROM "shop_app_product" WHERE "shop_app_product"."id" = 5 LIMIT 21; args=(5,); alias=default
SELECT "django_session"."session_key", "django_session"."session_data", "django_session"."expire_date" FROM "django_session" WHERE ("django_session"."expire_date" > '2024-04-15T12:24:46.206242+00:00'::timestamptz AND "django_session"."session_key" = 'uxuc5vptsz19e3w341xod6s623r7sxq1') LIMIT 21; args=(datetime.datetime(2024, 4, 15, 12, 24, 46, 206242, tzinfo=datetime.timezone.utc), 'uxuc5vptsz19e3w341xod6s623r7sxq1'); alias=default
SELECT "auth_user"."id", "auth_user"."password", "auth_user"."last_login", "auth_user"."is_superuser", "auth_user"."username", "auth_user"."first_name", "auth_user"."last_name", "auth_user"."email", "auth_user"."is_staff", "auth_user"."is_active", "auth_user"."date_joined" FROM "auth_user" WHERE "auth_user"."id" = 3 LIMIT 21; args=(3,); alias=default




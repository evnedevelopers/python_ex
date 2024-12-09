from django.urls import include, path

urlpatterns = [
    path("auth/", include(("api.v1.auth.urls", "api.v1.auth"), namespace="auth")),
    path("users/", include(("api.v1.users.urls", "api.v1.users"), namespace="users")),
    path(
        "profiles/",
        include(("api.v1.profiles.urls", "api.v1.profiles"), namespace="profiles"),
    ),
]

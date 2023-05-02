from . import views
from django.urls import path

urlpatterns = [
    path("", views.home, name="home"),
    path("logout-user", views.logout_user, name="logout_user"),
    path("login-admin/", views.login_user_admin, name="login_admin"),
    path("register-user-admin/", views.register_user_admin, name="register_user_admin"),
    path("config-admin/", views.config_admin, name="config_admin"),
    path("autenticacao-iqoption/", views.autenticao_iqoption, name="autenticacao_iqoption"),
    path("start-api/", views.start_api, name="start_api"),
    path("stop-api/", views.stop_api, name="stop_api"),
    path("config-admin-get/", views.config_admin_get, name="config_admin_get"),
    path("config-admin-post/", views.config_admin_post, name="config_admin_post"),
    path("query-results-operations-get-data-dashboard/", views.query_results_operations_get_data_dashboard, name="query_results_operations_get_data_dashboard"),

    # path("instrucoes-painel/", views.instrucoes_painel, name="instrucoes_painel"),
]
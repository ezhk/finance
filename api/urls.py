from django.urls import path, include
from rest_framework import routers

router = routers.SimpleRouter()
# router.register(r"code-bases", CodeBaseSet)
# router.register(r"code-executions", CodeExecutionSet)
# router.register(r"containers", ContainerSet)
# router.register(r"users", UserSet)
# router.register(r"history", UserCodeSet, basename="UserCode")

app_name = "api"
urlpatterns = [
    path("", include(router.urls)),
]

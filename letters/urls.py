from django.urls import path
from . import views

app_name = "letters"

urlpatterns = [
    path("", views.LetterListView.as_view(), name="list"),
    path("create/", views.LetterAddressCreateView.as_view(), name="create"),
    path(
        "create/<int:pk>/content/",
        views.LetterContentUpdateView.as_view(),
        name="create_content",
    ),
]

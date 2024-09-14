from django.urls import path
from projectApps.comments.api.views import CommentList, CommentDetail

app_name = "CommentsAPI"

urlpatterns = [
    path("list_create/", CommentList.as_view(), name="comment-list"),
    path("details/<int:pk>/", CommentDetail.as_view(), name="comment-detail"),
]

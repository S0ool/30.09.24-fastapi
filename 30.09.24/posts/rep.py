from posts.models import Post, User
from repository.repository import BaseRepository


class PostRepository(BaseRepository):
    model = Post

class UserRepository(BaseRepository):
    model = User

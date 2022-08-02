# Django User Activity

#### Tracking user activity in django including api hits, login, logout etc


## Example

##### In order to track api hit use ActivityLogMixin with class based API views and ViewSets.

```python
class PostReadOnlyViewSet(ActivityLogMixin, ReadOnlyModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_log_message(self, request) -> str:
        return f"{request.user} is reading blog posts"
```

from pdd_app.db.models import User, Category, Refresh
from sqladmin import ModelView


class UserAdmin(ModelView, model=User):
    column_list = [User.first_name, User.last_name]


class CategoryAdmin(ModelView, model=Category):
    column_list = [Category.category_name]


class RefreshAdmin(ModelView, model=Refresh):
    column_list = [Refresh.id]



from .wiews import UserAdmin, CategoryAdmin, RefreshAdmin
from fastapi import FastAPI
from sqladmin import Admin
from pdd_app.db.database import engine


def setup_admin(pdd_app: FastAPI):
    admin = Admin(pdd_app, engine)
    admin.add_view(UserAdmin)
    admin.add_view(CategoryAdmin)
    admin.add_view(RefreshAdmin)

from apps import app, db
from flask_admin import Admin, BaseView, expose,AdminIndexView
from flask_admin.contrib.sqla import ModelView
from apps.model import Books, BookSection, User, Album, AlbumTag, SeePower





admin = Admin(app, name='Admin', template_mode='bootstrap3')




# class MyView(BaseView):
#
#     @expose('/')
#     def index(self):
#
#         return self.render('admin_index.html')
#
# admin.add_view(MyView(name=u'Hello'))



admin.add_view(ModelView(User, db.session, name=u'用户', category=u'用户管理'))

admin.add_view(ModelView(Books, db.session, name=u'书籍', category=u'书籍管理'))
admin.add_view(ModelView(BookSection, db.session, name=u'章节', category=u'书籍管理'))

admin.add_view(ModelView(Album, db.session, name=u'相册', category=u'相册管理'))
admin.add_view(ModelView(AlbumTag, db.session, name=u'标签', category=u'相册管理'))
admin.add_view(ModelView(SeePower, db.session, name=u'权限', category=u'相册管理'))





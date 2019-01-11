from datetime import datetime

from apps import db


#用户表
class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    face = db.Column(db.String(200))
    sign = db.Column(db.TEXT)
    uuid = db.Column(db.String(80), unique=True, nullable=False)
    addtime = db.Column(db.DATETIME, index=True,default=datetime.now)
    # 指明关系,通过用户也能找到相册
    albums = db.relationship('Album', backref='user')
    album_loves = db.relationship('AlbumLove', backref='user')


    def __repr__(self):
        return '<User %r>' % self.name

#相册标签
class AlbumTag(db.Model):
    __tablename__ = 'album_tag'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    #指明关系,通过标签也能找到相册
    albums = db.relationship('Album', backref='album_tag')

    def __repr__(self):
        return '<AlbumTag %r>' % self.name


#权限
class SeePower(db.Model):
    __tablename__ = 'see_power'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)

    # albums = db.relationship('Album', backref='see_power')

    def __repr__(self):
        return '<SeePower %r>' % self.name



#相册表
class Album(db.Model):
    __tablename__ = 'album'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    album_sign = db.Column(db.TEXT)
    photo_num = db.Column(db.Integer, default=0)
    click_num = db.Column(db.Integer, default=0)
    love_num = db.Column(db.Integer, default=0)
    addtime = db.Column(db.DATETIME, index=True, default=datetime.now)

    #外键
    power_id = db.Column(db.Integer, db.ForeignKey('see_power.id'))
    tag_id = db.Column(db.Integer, db.ForeignKey('album_tag.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    album_loves = db.relationship('AlbumLove', backref='album')
    photos = db.relationship('Photo', backref='album')

    def __repr__(self):
        return '<Album %r>' % self.title


#喜欢的相册(收藏)
class AlbumLove(db.Model):
    __tablename__ = 'album_love'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    album_id = db.Column(db.Integer, db.ForeignKey('album.id'))
    addtime = db.Column(db.DATETIME, index=True, default=datetime.now)

#图片表
class Photo(db.Model):
    __tablename__ = 'photo'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True, nullable=False)#原本图像
    name_small = db.Column(db.String(200), unique=True, nullable=False)#缩略图
    name_show = db.Column(db.String(200), unique=True, nullable=False)  # 展示图
    album_id = db.Column(db.Integer, db.ForeignKey('album.id'))
    addtime = db.Column(db.DATETIME, index=True, default=datetime.now)



#小说
class Books(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    book_name = db.Column(db.String(80), unique=True)
    book_writer = db.Column(db.String(80))
    book_desc = db.Column(db.String(500))
    book_url = db.Column(db.String(200))
    book_img = db.Column(db.String(200))




class BookSection(db.Model):
    __tablename__ = 'book_section'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    section_url = db.Column(db.String(200))
    section_title = db.Column(db.String(80))
    books_id = db.Column(db.Integer, db.ForeignKey('books.id'))


class BookContent(db.Model):
    __tablename__ = 'book_content'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text)

    book_section_id = db.Column(db.Integer, db.ForeignKey('book_section.id'))






#文章标签
class ArticleTag(db.Model):
    __tablename__ = 'article_tag'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    #指明关系,通过标签也能找到文章
    articles = db.relationship('Article', backref='article_tag')






#文章表
class Article(db.Model):
    __tablename__ = 'article'

    id = db.Column(db.Integer, primary_key=True)
    article_title = db.Column(db.String(80), nullable=False)
    article_img_url = db.Column(db.String(200))
    article_writer = db.Column(db.String(20))
    article_desc = db.Column(db.String(200))
    article_text = db.Column(db.TEXT)
    click_num = db.Column(db.Integer, default=0)
    addtime = db.Column(db.DATETIME, index=True, default=datetime.now)

    #外键
    power_id = db.Column(db.Integer, db.ForeignKey('see_power.id'))
    articletag_id = db.Column(db.Integer, db.ForeignKey('article_tag.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class RandomImg(db.Model):
    __tablename__ = 'random_img'

    id = db.Column(db.Integer, primary_key=True)
    img_url = db.Column(db.String(200))



class WebClick(db.Model):
    __tablename__ = 'web_click'

    id = db.Column(db.Integer, primary_key=True)
    click_num = db.Column(db.Integer, default=1)


class AboutMsg(db.Model):
    __tablename__ = 'aboutmsg'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100))
    user_name = db.Column(db.String(30))
    user_face_url = db.Column(db.String(200))
    addtime = db.Column(db.DATETIME, index=True, default=datetime.now)


class AdminTag(db.Model):
    __tablename__ = 'admin_tag'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))



if __name__ == '__main__':
    i = 0
    if i == 0:
        #初始化数据库失败，切记循环引用问题
        db.drop_all()
        db.create_all()

        tag0 = AlbumTag(name='美女')
        tag1 = AlbumTag(name='风景')
        tag2 = AlbumTag(name='动漫')
        tag3 = AlbumTag(name='写真')
        tag4 = AlbumTag(name='萌物')
        tag5 = AlbumTag(name='游戏')
        tag6 = AlbumTag(name='纪实')
        tag7 = AlbumTag(name='美食')
        tag8 = AlbumTag(name='影视')
        tag9 = AlbumTag(name='建筑')
        tag10 = AlbumTag(name='节日')
        tag11 = AlbumTag(name='静物')

        power0 = SeePower(name='所有人')
        power1 = SeePower(name='仅自己')

        tag20 = ArticleTag(name='linux')
        tag21 = ArticleTag(name='python')
        tag22 = ArticleTag(name='javascript')
        tag23 = ArticleTag(name='bootstrap')
        tag24 = ArticleTag(name='java')
        tag25 = ArticleTag(name='html')
        tag26 = ArticleTag(name='css')
        tag27 = ArticleTag(name='windows')
        tag28 = ArticleTag(name='flask')
        tag29 = ArticleTag(name='spider')
        tag30 = ArticleTag(name='other')
        db.session.add(tag0)
        db.session.add(tag1)
        db.session.add(tag2)
        db.session.add(tag3)
        db.session.add(tag4)
        db.session.add(tag5)
        db.session.add(tag6)
        db.session.add(tag7)
        db.session.add(tag8)
        db.session.add(tag9)
        db.session.add(tag10)
        db.session.add(tag11)

        db.session.add(power0)
        db.session.add(power1)

        db.session.add(tag20)
        db.session.add(tag21)
        db.session.add(tag22)
        db.session.add(tag23)
        db.session.add(tag24)
        db.session.add(tag25)
        db.session.add(tag26)
        db.session.add(tag27)
        db.session.add(tag28)
        db.session.add(tag29)
        db.session.add(tag30)

        db.session.commit()


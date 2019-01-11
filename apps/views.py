from apps import app, db
from flask import render_template, request, session, redirect, url_for, flash, make_response
from functools import wraps
import os, shutil, requests
from apps.forms import LoginForm, InfoForm, RegistForm, PasswordForm, \
    AlubmCreateForm, AlubmUpload, ArticleCreateForm, AboutMsgForm

from apps.model import User, Album, Photo, AlbumTag, AlbumLove, Books, \
    BookSection, BookContent, Article, ArticleTag, RandomImg, WebClick, AboutMsg, AdminTag

from flask_uploads import UploadSet, IMAGES, configure_uploads
from uuid import uuid4
from datetime import datetime
from apps.utils import create_thumbnail, create_show, create_face
from bs4 import BeautifulSoup
import random





#2.产生UploadSet类对象实例,管理上传集合
facephoto = UploadSet('face', IMAGES)
albumphoto = UploadSet('photo', IMAGES)
#3.绑定app与UploadSet对象实例， app和Uploads协同工作
configure_uploads(app, facephoto)
configure_uploads(app, albumphoto)

headers = {
        "Host": "www.biquge5200.cc",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:63.0) Gecko/20100101 Firefox/63.0"
    }



#装饰器登录检查,f:被装饰函数,next指明下一次跳转
def user_login_req(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_name' not in session:
            return redirect(url_for('user_login', next=request.url))
        return f(*args, **kwargs)

    return decorated_function




@app.route('/')
def index():
    articles = Article.query.filter(Article.power_id != 2, Article.id < 6).order_by(Article.addtime.desc()).all()
    click = WebClick.query.filter_by(id=1).first()
    click.click_num += 1
    db.session.add(click)
    db.session.commit()
    return render_template('index.html', articles=articles)



@app.route('/user/login/', methods=['GET', 'POST'])
def user_login():

    form = LoginForm()
    if form.validate_on_submit():
        username = request.form['user_name']
        userpassword = (request.form['user_password'])

        user_x = User.query.filter_by(name=username).first()

        if user_x:
            if str(userpassword) == str(user_x.password):
                flash('登录成功', category='ok')
                #写入会话
                session['user_name'] = user_x.name
                session['user_id'] = user_x.id

                return redirect(url_for('index'))
            else:
                flash('密码输入错误', category='err')
                return render_template('user_login.html', form=form)
        else:
            flash('用户不存在', category='err')
            return render_template('user_login.html', form=form)

    return render_template('user_login.html', form=form)



#退出
@app.route('/user/logout/')
def logout():
    #session实质就是一个字典
    session.pop('user_name', None)
    return redirect(url_for('index'))



@app.route('/user/regist/', methods=['GET', 'POST'])
def user_regist():
    form = RegistForm()
    if form.validate_on_submit():

        user_name = request.form['user_name']

        #判断用户是否存在
        user_x = User.query.filter_by(name=user_name).first()
        if user_x:
            flash('用户已经存在', category='err')
        else:
            user = User()
            user.name = user_name
            user.password = request.form['user_password']
            user.email = request.form['user_email']
            user.phone = request.form['user_phone']
            user.sign = request.form['user_sign']
            user.uuid = str(uuid4().hex)
            # 获取头像文件，是一个对象(文件名,属性)
            filestorage = request.files['user_face']
            # 头像文件名称
            if filestorage.filename != '':

                fix = '.' + str(filestorage.filename).split('.')[-1]
                name = str(uuid4().hex) + fix
                folder = user.uuid
                try:
                    fname = facephoto.save(storage=filestorage, folder=folder, name=name)
                    # 创建保存压缩图返回文件名
                    fname_small = create_face(path=os.path.join(app.config['USERS_FACEFILES'], folder),
                                                   filename=name, base_width=200)

                    fpath = facephoto.path(fname)
                    os.remove(fpath)
                except Exception as i:
                    print(i)
                    return render_template('404.html')
                user.face = fname_small

            """写入"""
            db.session.add(user)
            db.session.commit()

            flash('注册成功', category='ok')
            return redirect(url_for('user_login', username=user.name))

    return render_template('user_regist.html', form=form)



@app.route('/user/center/')
@user_login_req
def user_center():

    imgs = RandomImg.query.filter_by(id=int(random.randint(1, 10))).first()

    return render_template('user_center.html', imgs=imgs)



@app.route('/user/detail/')
@user_login_req
def user_detail():

    user = User.query.filter_by(name=session.get('user_name')).first()

    face_url = facephoto.url(user.uuid + '/' + user.face)

    return render_template('user_detail.html', user=user, face_url=face_url)



@app.route('/user/password/', methods=['POST', 'GET'])
@user_login_req
def user_password():
    form = PasswordForm()
    if form.validate_on_submit():

        oldpassword = request.form['old_password']
        newpassword = request.form['new_password']
        user = User.query.filter_by(name=session.get('user_name')).first()

        if str(oldpassword) == str(user.password):
            user.password = newpassword
            #自动判断插入或者更新
            db.session.add(user)
            db.session.commit()
            session.pop('user_mame', None)
            flash('修改密码成功, 请重新登录', category='ok')
            return redirect(url_for('user_login', username=user.name))

        else:
            flash('旧密码输入有误', category='err')
            return render_template('user_password.html', form=form)

    return render_template('user_password.html', form=form)



@app.route('/user/info/', methods=['POST', 'GET'])
@user_login_req
def user_info():
    form = InfoForm()
    user = User.query.filter_by(name=session.get('user_name')).first()
    if request.method == 'GET':
        form.user_sign.data = user.sign


    if form.validate_on_submit():

        user.name = request.form['user_name']
        user.email = request.form['user_email']
        user.phone = request.form['user_phone']

        user.sign = form.user_sign.data
        filestorage = form.user_face.data

        try:
            # 头像文件名称
            if filestorage.filename != '':
                folder = user.uuid

                # 删除旧的
                oldpath = facephoto.path(filename=folder + '/' + user.face)
                print(oldpath)
                os.remove(oldpath)

                fix = '.' + str(filestorage.filename).split('.')[-1]
                name = str(uuid4().hex) + fix

                try:
                    fname = facephoto.save(storage=filestorage, folder=folder, name=name)
                    # 创建保存压缩图返回文件名
                    fname_small = create_face(path=os.path.join(app.config['USERS_FACEFILES'], folder),
                                              filename=name, base_width=500)

                    fpath = facephoto.path(fname)
                    os.remove(fpath)
                except:
                    return render_template('404.html')

                user.face = fname_small
        except:
            user.face = user.face
            #ps:2018.12.27晚，苦思冥想想出捕获异常这种办法,不然真要强制上传face了 哈哈
            #ps:2018.12.30 青涩!把之前注册和修改都弄个压缩图片，调用pli, 先保存原图,再把原图压缩，删除原图,前端调用的压缩的url
            #               感觉后端调用这种api,不管怎么弄服务器多少都有点压力,毕竟涉及到一次删除,如果可以放到前端就好了, 菜！
        #更新数据库
        db.session.add(user)
        db.session.commit()
        session['user_name'] = user.name

        return redirect(url_for('user_detail'))

    return render_template('user_info.html', user=user, form=form)


@app.route('/user/del/', methods=['POST', 'GET'])
@user_login_req
def user_del():
    if request.method == 'POST':
        password2 = request.form['new_password2']
        user = User.query.filter_by(name=session.get('user_name')).first()
        albums = Album.query.filter_by(user_id=user.id).all()
        #这个有没有不需要遍历单个数据，直接清除列表那种
        for album in albums:
            photos = Photo.query.filter_by(album_id=album.id).all()
            for photo in photos:
                db.session.delete(photo)
                db.session.commit()
            db.session.delete(album)
            db.session.commit()


        if str(password2) == str(user.password):

            #uuid没有保存到session,通过数据库获取即可
            #删除文件
            del_path = os.path.join(app.config['USERS_FACEFILES'], str(user.uuid))
            del_path2 = os.path.join(app.config['USERS_PHOTOS'], str(user.uuid))
            shutil.rmtree(del_path)
            shutil.rmtree(del_path2)
            # 删除数据
            db.session.delete(user)
            db.session.commit()

            flash('注销成功', category='ok')
            return redirect(url_for('logout'))
        else:
            flash('密码输入有误，请重新输入', category='err')
            return render_template('user_del.html')

    return render_template('user_del.html')




# #创建相册
@app.route('/album/create', methods=['GET', 'POST'])
@user_login_req
def album_create():

    form = AlubmCreateForm()
    if form.validate_on_submit():
        album_title = form.album_title.data
        album_sign = form.album_sign.data
        see_power = form.see_power.data
        album_tag = form.album_tag.data
        #ps:2018.12.29
        if Album.query.filter_by(title=album_title).first():
            flash('要创建的相册已经存在', category='err')
            return redirect(url_for('album_create'))

        album = Album(title=album_title, album_sign=album_sign,
                      power_id=see_power, tag_id=album_tag,
                      user_id=int(session.get('user_id')))

        db.session.add(album)
        db.session.commit()

        return redirect(url_for('album_upload'))

    return render_template('album_create.html', form=form)


#上传图片
@app.route('/album/upload', methods=['GET', 'POST'])
@user_login_req
def album_upload():
    form = AlubmUpload()
    #ps:2018.12.30 此处更改，针对个人查询
    albums = Album.query.filter_by(user_id=session.get('user_id')).all()
    print(albums)
    form.album_title.choices = [(album.id, album.title) for album in albums]

    if form.validate_on_submit():
        user = User.query.filter_by(name=session.get('user_name')).first()
        album = Album.query.filter_by(id=form.album_title.data).first()

        #按照列表接收文件
        filelist = request.files.getlist('album_photo')

        success = 0
        fail = 0
        smallurl_list = []

        start = datetime.now().strftime('%S')
        for filestorage in filelist:
            if filestorage.filename != '':
                fix = '.' + str(filestorage.filename).split('.')[-1]
                name = uuid4().hex + fix
                folder = user.uuid + '/' + album.title
                try:
                    pname = albumphoto.save(storage=filestorage, folder=folder, name=name)
                    photo_name = pname.split('/')[-1]
                    # 创建保存缩略图返回文件名，并根据文件名获取url
                    pname_small = create_thumbnail(path=os.path.join(app.config['USERS_PHOTOS'], folder),
                                                   filename=photo_name, base_width=300)
                    pname_smallurl = albumphoto.url(folder + '/' + pname_small)
                    smallurl_list.append(pname_smallurl)
                    # 创建保存展示图返回文件名，并根据文件名获取url
                    pname_show = create_show(path=os.path.join(app.config['USERS_PHOTOS'], folder),
                                                   filename=photo_name, base_width=800)

                    #写入数据库
                    photo = Photo(name=pname, name_small=pname_small,
                                  name_show=pname_show, album_id=album.id)
                    db.session.add(photo)
                    db.session.commit()

                    #删除原图
                    fpath = albumphoto.path(filename=pname)
                    os.remove(fpath)
                    success += 1
                except:
                    fail += 1

        #ps:2018.12.30pm 优化标题生成和删除操作
        #照片总量
        album.photo_num += success
        db.session.add(album)
        db.session.commit()

        end = datetime.now().strftime('%S')
        flash('目前相册共有%s张,本次上传成功%s张,失败%s张,共用时%s秒'%
              (album.photo_num, success, fail, (float(end) - float(start))), category='ok')
        return render_template('album_upload.html', form=form, smallurl_list=smallurl_list)


    return render_template('album_upload.html', form=form)


@app.route('/album/list/<int:page>')
def album_list(page):
    albumtags = AlbumTag.query.order_by(AlbumTag.id).all()
    tagid = request.args.get('tag')
    if tagid != None:
        albums = Album.query.filter(Album.power_id != 3, Album.tag_id == int(tagid)).\
            order_by(Album.addtime.desc()).paginate(page=page, per_page=8)
    else:
        albums = Album.query.filter(Album.power_id != 3).order_by(Album.addtime.desc()).paginate(page=page, per_page=8)

    for album in albums.items:
        try:
            title_photo = album.photos[0].name_small
            title_uuid = album.photos[0].name
            folder = (os.path.split(title_uuid))[0] + '/' + title_photo
            global titleurl
            titleurl = albumphoto.url(filename=folder)

        except:
            pass
        # 追加对象
        album.titleurl = titleurl


    return render_template('album_list.html', albumtags=albumtags, albums=albums)


@app.route('/album/browse/<int:id>')
def album_browse(id):
    album = Album.query.get(int(id))

    # 点击量
    album.click_num += 1
    db.session.add(album)
    db.session.commit()
    # 查询推荐
    recommd_albums = Album.query.filter(Album.tag_id == album.tag_id, Album.id != album.id).all()

    # 推荐封面
    for item in recommd_albums:
        try:
            title_photo = item.photos[0].name_small
            title_uuid = item.photos[0].name
            folder2 = (os.path.split(title_uuid))[0] + '/' + title_photo
            global titleurl
            titleurl = albumphoto.url(filename=folder2)
        except:
            pass
        # 追加对象
        item.url = titleurl
    #我的收藏
    favor_albums = []
    if 'user_id' in session:
        user = User.query.get(int(session.get('user_id')))
        #已收藏的相册列表
        for favor in user.album_loves:
            favor_albums.append(favor.album)
        #追加对象前计划好列表和对象关系
        for falbum in favor_albums:
            try:
                title_photo3 = falbum.photos[0].name_small
                title_uuid3 = falbum.photos[0].name
                folder3 = (os.path.split(title_uuid3))[0] + '/' + title_photo3
                global titleurl3
                titleurl3 = albumphoto.url(filename=folder3)
                print(titleurl3)
            except:
                pass
            # 追加对象
            falbum.titleurl3 = titleurl3


    #头像
    face_url = facephoto.url(album.user.uuid + '/' + album.user.face)
    for photo in album.photos:
        folder = (os.path.split(photo.name))[0] + '/' + photo.name_show

        photourl = albumphoto.url(filename=folder)
        #追加对象
        photo.url = photourl
    temp = render_template('album_browse.html', album=album, face_url=face_url,
                           recommd_albums=recommd_albums, favor_albums=favor_albums)

    return temp


@app.route('/album/favor/', methods=['GET'])
def album_favor():
    #获取参数
    aid = request.args.get('aid')
    uid = request.args.get('uid')
    print(aid)
    #查询判断
    existed = AlbumLove.query.filter_by(user_id=uid, album_id=aid).count()
    album = Album.query.filter_by(id=aid).first()

    if existed >= 1:
        res = {'ok': 0}
    else:

        favor = AlbumLove(user_id=uid, album_id=aid)
        #收藏量
        album.love_num += 1
        db.session.add(album)
        db.session.add(favor)
        db.session.commit()
        res = {'ok': 1}

    import json
    return json.dumps(res)


@app.route('/user/album/favor/')
def user_album_favor():

    love_albumlist = []
    albumloves = AlbumLove.query.filter_by(user_id=session.get('user_id')).all()
    for albumlove in albumloves:

        album_id = albumlove.album_id
        love_album = Album.query.filter_by(id=album_id).order_by(Album.addtime.desc()).first()
        love_albumlist.append(love_album)

    for love_album in love_albumlist:
        try:
            title_photo = love_album.photos[0].name_small
            title_uuid = love_album.photos[0].name
            folder = (os.path.split(title_uuid))[0] + '/' + title_photo
            global titleurl
            titleurl = albumphoto.url(filename=folder)

        except:
            pass
        # 追加对象
        love_album.titleurl = titleurl


    return render_template('user_album_favor.html', love_albumlist=love_albumlist)





@app.route('/user/album/mine/')
def user_album_mine():


    albums = Album.query.filter_by(user_id=session.get('user_id')).order_by(Album.addtime.desc()).all()

    for album in albums:
        try:
            title_photo = album.photos[0].name_small
            title_uuid = album.photos[0].name
            folder = (os.path.split(title_uuid))[0] + '/' + title_photo
            global titleurl
            titleurl = albumphoto.url(filename=folder)

        except:
            pass
        # 追加对象
        album.titleurl = titleurl

    return render_template('user_album_mine.html', albums=albums)

#取消关注
@app.route('/user/album/favor/del/<int:id>')
def user_album_favor_del(id):

    albumlove = AlbumLove.query.filter_by(user_id=session.get('user_id'),
                                           album_id=int(id)).first()
    print(albumlove)
    db.session.delete(albumlove)
    db.session.commit()
    return redirect(url_for('user_album_favor'))





#bookname
@app.route('/book/list/')
def book_list():
    book = Books.query.all()
    if book == []:
        url = 'https://www.biquge5200.cc/xuanhuanxiaoshuo/'
        response = requests.get(url, headers=headers)

        response.encoding = 'gbk'
        after_bs = BeautifulSoup(response.text, 'lxml')

        new_updata = after_bs.find_all('div', class_='l')  # div class=l标签 包裹的内容
        after_new_updata = BeautifulSoup(str(new_updata), 'lxml')

        span2 = after_new_updata.find_all('span', class_='s2')  # 继续筛选书籍
        span5 = after_new_updata.find_all('span', class_='s5')  # 继续筛选作者

        writer_list = []  # 作者list
        for sp5 in span5:
            writer_list.append(sp5.text)

        after_span2 = BeautifulSoup(str(span2), 'lxml')

        a_list = after_span2.find_all('a')
        for a in a_list:
            book_name = a.text  # ----------------小说名
            book_x = Books.query.filter_by(book_name=book_name).first()

            if book_x is None:
                book_url = a.get('href')  # ------------------小说url
                try:
                    writer = writer_list.pop(0)  # -----------------作者
                    book = Books(book_name=book_name, book_writer=writer, book_url=book_url)
                    db.session.add(book)
                    db.session.commit()

                except:
                    pass

    books = Books.query.all()
    return render_template('book_list.html', books=books)

#章节
@app.route('/book/browse/<int:page>')
def book_browse(page):
    page = int(page)
    id = request.args.get('id')
    book = Books.query.get(int(id))

    if book.book_desc == None:
        url = book.book_url
        response = requests.get(url, headers=headers)
        response.encoding = 'gbk'

        after_bs = BeautifulSoup(response.text, 'lxml')

        div_fmimg = after_bs.find('div', id="fmimg")
        img_list = div_fmimg('img')
        for a in img_list:
            img_url = a.get('src')  # ------------图片url
            book.book_img = img_url

        div_intro = after_bs.find('div', id="intro")
        book_desc = div_intro.text  # -----------------------小说简介
        book.book_desc = book_desc
        # ps:2019.1.4  updata book's table
        db.session.add(book)
        db.session.commit()

        """章节部分"""

        dl = after_bs.find_all('dl')
        after_new_updata = BeautifulSoup(str(dl), 'lxml')
        dd_list = after_new_updata.find_all('dd')

        after_dd = BeautifulSoup(str(dd_list), 'lxml')
        a_list = after_dd.find_all('a')

        num = len(a_list) - 9
        for i in range(num):
            section_url = a_list[9 + i].get('href')  # ---------------小说章节url
            section_title = a_list[9 + i].text  # --------------------小说章节标题

            sections = BookSection(section_url=section_url, section_title=section_title, books_id=int(id))
            db.session.add(sections)
            db.session.commit()

    booksections= BookSection.query.filter_by(books_id=int(id)).paginate(page=page, per_page=8)
    count = BookSection.query.filter_by(books_id=int(id)).count()

    if (count/8) > int(count/8):
        count_page = int(count/8) + 1
    else:
        count_page = int(count/8)


    return render_template('book_browse.html', book=book, booksections=booksections, page=page, count_page=count_page)

#正文
@app.route('/book/content/<int:id>')
def book_content(id):
    bookcontent = BookContent.query.filter_by(book_section_id=int(id)).first()
    if bookcontent is None:
        bsc = BookSection.query.get(int(id))
        url = bsc.section_url
        response = requests.get(url, headers=headers)
        response.encoding = 'gbk'
        after_bs = BeautifulSoup(response.text, 'lxml')

        div_content = after_bs.find('div', id="content")  # -------------------小说正文

        content_p = BeautifulSoup(str(div_content), 'lxml')
        content = content_p.text

        contents = BookContent(content=content, book_section_id=int(id))
        db.session.add(contents)
        db.session.commit()

    bookcontent = BookContent.query.filter_by(book_section_id=int(id)).first()
    return render_template('book_content.html', bookcontent=bookcontent, id=id)





@app.route('/article/create/', methods=['GET', 'POST'])
@user_login_req
def article_create():

    form = ArticleCreateForm()
    if form.validate_on_submit():
        article_title = form.article_title.data
        article_img_url = form.article_img_url.data
        article_desc = form.article_desc.data
        see_power = form.see_power.data
        article_tag = form.article_tag.data
        article_text = form.article_text.data

        user_id = int(session.get('user_id'))

        if Article.query.filter_by(article_title=article_title).first():
            flash('要创建的文章标题已经存在', category='err')
            return redirect(url_for('article_create'))

        article = Article(article_title=article_title,
                          article_img_url=article_img_url,
                          article_writer=str(session.get('user_name')),
                          article_desc=article_desc,
                          power_id=see_power,
                          articletag_id=article_tag,
                          article_text=article_text,
                          user_id=user_id)

        db.session.add(article)
        db.session.commit()
        showart = Article.query.filter_by(article_title=article_title).first()
        flash('创建成功', category='ok')
        return render_template('article_create.html', form=form, showart=showart)

    return render_template('article_create.html', form=form)


@app.route('/article/list/<int:page>')
def article_list(page):
    tagid = request.args.get('tag')

    if tagid != None:
        articles = Article.query.filter(Article.power_id != 2, Article.articletag_id == int(tagid)).\
            order_by(Article.addtime.desc()).paginate(page=page, per_page=5)
    else:
        articles = Article.query.filter(Article.power_id != 2).order_by(Article.addtime.desc()).\
                                            paginate(page=page, per_page=5)



    articletags = ArticleTag.query.order_by(ArticleTag.id).all()
    return render_template('article_list.html', articles=articles, articletags=articletags)


@app.route('/article/content/<int:id>')
def article_content(id):

    article = Article.query.filter_by(id=int(id)).first()
    user = User.query.filter_by(id=article.user_id).first()
    article.click_num += 1
    db.session.add(user)
    db.session.commit()
    return render_template('article_content.html', article=article, user=user)




@app.route('/about/me/<int:page>', methods=['GET', 'POST'])
def about_me(page):
    form = AboutMsgForm()
    if form.validate_on_submit():
        user_name = session.get('user_name')
        if user_name:
            about_msg = form.about_msg.data
            user = User.query.filter_by(name=session.get('user_name')).first()
            user_face_url = facephoto.url(user.uuid + '/' + user.face)
            aboutmsg = AboutMsg(content=about_msg, user_name=user_name, user_face_url=user_face_url)
            db.session.add(aboutmsg)
            db.session.commit()
        else:
            flash('请先登录', category='err')
            return redirect(url_for('about_me', page=1))

    article_num = Article.query.count()
    album_num = Album.query.count()
    num = WebClick.query.filter_by(id=1).first()

    aboutmsgs = AboutMsg.query.order_by(AboutMsg.addtime.desc()).paginate(page=page, per_page=5)


    return render_template('about_me.html', article_num=article_num,
                           album_num=album_num, num=num, form=form,
                           aboutmsgs=aboutmsgs)




@app.route('/about/del/msg/<int:id>')
def about_del_msg(id):
    about_msg = AboutMsg.query.filter_by(id=int(id)).first()
    db.session.delete(about_msg)
    db.session.commit()
    flash('删除成功', category='ok')
    return redirect(url_for('about_me', page=1))




#管理员
@app.route('/admin/user/info/')
@user_login_req
def admin_user_info():
    user_name = session.get('user_name')
    user_id = session['user_id']
    if str(user_name) == '夜雨听风' and str(user_id) == '1':
        users = User.query.all()
        return render_template('admin_user_info.html', users=users)
    else:
        flash('you are not admin!', category='ok')
        return redirect(url_for('index'))




@app.route('/admin/user/article/')
@user_login_req
def admin_user_article():
    user_name = session.get('user_name')
    user_id = session['user_id']
    admintag = AdminTag.query.filter_by(id=1).first()
    if admintag:
        if str(user_name) == str(admintag.name) and str(user_id) == '1':
            return render_template('admin_user_article.html')
        else:
            flash('you are not admin!', category='ok')
            return redirect(url_for('index'))
    else:
        flash('you are not admin!', category='ok')
        return redirect(url_for('index'))

@app.route('/user/music/')
def user_music():

    return render_template('user_music.html')








@app.errorhandler(404)
def page_not_found(err):
    #在响应头添加信息
    resp = make_response(render_template('404.html'),404)
    resp.headers['X-SS'] = 'hello'
    return resp



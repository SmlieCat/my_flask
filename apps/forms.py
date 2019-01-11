from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField,SubmitField,PasswordField,TextAreaField,SelectField
from wtforms.validators import DataRequired,EqualTo,Length

from apps.model import AlbumTag, SeePower, ArticleTag

powers = SeePower.query.order_by(SeePower.id).all()
tags = AlbumTag.query.order_by(AlbumTag.id).all()

article_tags = ArticleTag.query.order_by(ArticleTag.id).all()



class RegistForm(FlaskForm):
    user_name = StringField(
        label='用户名',
        validators=[Length(min=2, max=7, message='长度为2到7个字符'),
            DataRequired(message='用户名不能为空')],
        render_kw={"id":"user_name",
                   "class":"form-control",
                   "placeholder":"输入用户名"}
    )

    user_password = PasswordField(
        label='密码',
        validators=[Length(min=3, max=10, message='长度为3到10个字符'),
            DataRequired(message='密码不能为空')],
        render_kw={"id": "user_password",
                   "class": "form-control",
                   "placeholder": "输入密码"}
    )

    user_password2 = PasswordField(
        label='确认密码',
        validators=[EqualTo('user_password', message='密码不一致')],
        render_kw={"id": "user_password2",
                   "class": "form-control",
                   "placeholder": "确认密码"}
    )

    user_email = StringField(
        label='邮箱',
        validators=[Length(min=0, max=20, message='长度为0到20个字符')],
        render_kw={"id": "user_email",
                   "class": "form-control",
                   "placeholder": "输入邮箱"}
    )

    user_phone = StringField(
        label='联系方式',
        validators=[Length(min=0, max=20, message='长度为0到20个字符')],
        render_kw={"id": "user_phone",
                   "class": "form-control",
                   "placeholder": "输入联系方式"}
    )



    user_sign = TextAreaField(
        label='签名',
        validators= [Length(min=0, max=200, message='长度为0到200个字符')],
        render_kw={"id": "user_sign",
                   "class": "form-control",
                   "placeholder": "填写签名"}
    )

    user_face = FileField(
        label='头像',
        validators=[FileRequired(message='头像不能为空'),
                    FileAllowed(['jpg', 'jpeg', 'png'], '只允许图像格式为:%s' % str(['jpg', 'jpeg', 'png']))],
        render_kw={"id": "user_face",
                   "class": "form-control",
                   "placeholder": "插入头像"}
    )



    submit = SubmitField(
        label='提交',
        render_kw={"class":"btn btn-success",
                   "value": "注册"}

    )



class LoginForm(FlaskForm):
    user_name = StringField(
        label='用户名',
        validators=[DataRequired(message='用户名不能为空')],
        render_kw={"id": "user_name",
                   "class": "form-control",
                   "placeholder": "输入用户名"}
    )

    user_password = PasswordField(
        label='密码',
        validators=[DataRequired(message='密码不能为空')],
        render_kw={"id": "user_password",
                   "class": "form-control",
                   "placeholder": "输入密码"}
    )

    submit = SubmitField(
        label='提交',
        render_kw={"class": "btn btn-success",
                   "value": "登录"}

    )



class PasswordForm(FlaskForm):
    old_password = PasswordField(
        label='旧密码',
        validators=[DataRequired(message='旧密码不能为空')],
        render_kw={"id": "old_password",
                   "class": "form-control",
                   "placeholder": "输入旧密码"}
    )

    new_password = PasswordField(
        label='新密码',
        validators=[Length(min=3, max=10, message='长度为3到10个字符'),
            DataRequired(message='新密码不能为空')],
        render_kw={"id": "new_password",
                   "class": "form-control",
                   "placeholder": "输入新密码"}
    )

    new_password2 = PasswordField(
        label='确认新密码',
        validators=[EqualTo('new_password', message='密码不一致')],
        render_kw={"id": "new_password2",
                   "class": "form-control",
                   "placeholder": "确认新密码"}
    )

    submit = SubmitField(
        label='提交',
        render_kw={"class": "btn btn-primary",
                   "value": "确认修改"}

    )



class InfoForm(FlaskForm):
    user_name = StringField(
        label='用户名',
        validators=[Length(min=2, max=7, message='长度为2到7个字符'),
            DataRequired(message='用户名不能为空')],
        render_kw={"id": "user_name",
                   "class": "form-control",
                   "placeholder": "修改用户名"}
    )


    user_email = StringField(
        label='邮箱',
        validators=[Length(min=0, max=20, message='长度为0到20个字符')],
        render_kw={"id": "user_email",
                   "class": "form-control",
                   "placeholder": "修改邮箱"}
    )

    user_phone = StringField(
        label='联系方式',
        validators=[Length(min=0, max=20, message='长度为0到20个字符')],
        render_kw={"id": "user_phone",
                   "class": "form-control",
                   "placeholder": "修改联系方式"}
    )


    user_sign = TextAreaField(
        label='签名',
        validators=[Length(min=0, max=50, message='长度为0到50个字符')],
        render_kw={"id": "user_sign",
                   "class": "form-control",
                   "placeholder": "填写签名"}
    )


    user_face = FileField(
        label='头像',
        validators=[
                    FileAllowed(['jpg', 'jpeg', 'png'], '只允许图像格式为:%s' % str(['jpg', 'jpeg', 'png']))],
        render_kw={"id": "user_face",
                   "class": "form-control",
                   "placeholder": "修改头像"}
    )






    submit = SubmitField(
        label='提交',
        render_kw={"class": "btn btn-primary",
                   "value": "确认修改"}

    )


class AlubmCreateForm(FlaskForm):
    album_title = StringField(
        label='相册标题',
        validators=[Length(min=2, max=15, message='长度为2到15个字符'),
                    DataRequired(message='相册标题不能为空')],
        render_kw={"id": "album_title",
                   "class": "form-control",
                   "placeholder": "填写相册标题"}
    )

    album_sign = TextAreaField(
            label='相册描述',
            validators=[Length(min=0, max=200, message='最长为200个字符')],
            render_kw={"id": "album_sign",
                       "class": "form-control",
                       "placeholder": "填写相册描述"}
        )

    see_power = SelectField(
        label='相册浏览权限',
        validators=[DataRequired(message='相册权限不能为空')],
        coerce=int,
        choices=[(power.id, power.name) for power in powers],
        render_kw={"id": "see_power",
                   "class": "form-control"}
    )

    album_tag = SelectField(
        label='相册类别',
        validators=[DataRequired(message='相册类别不能为空')],
        coerce=int,
        choices=[(tag.id, tag.name) for tag in tags],

        render_kw={"id": "album_tag",
                   "class": "form-control"}
    )

    submit = SubmitField(
        label='开始创建',
        render_kw={"class": "btn btn-primary",
                   "value": "开始创建"}

    )



class AlubmUpload(FlaskForm):

    album_title = SelectField(
        label='相册标题',
        validators=[DataRequired(message='相册标题不能为空')],
        coerce=int,

        render_kw={"id": "album_title",
                   "class": "form-control"}
    )

    album_photo = FileField(
        label='图片',
        validators=[FileRequired(message='图片不能为空'),
                    FileAllowed(['jpg', 'jpeg', 'png'], '只允许图像格式为:%s' % str(['jpg', 'jpeg', 'png']))],
        render_kw={"id": "album_photo",
                   "class": "form-control",
                   'multiple': 'multiple'}
    )

    submit = SubmitField(
        label='开始上传',
        render_kw={"class": "btn btn-primary",
                   "value": "开始上传"}

    )



class ArticleCreateForm(FlaskForm):
    article_title = StringField(
        label='文章标题',
        validators=[Length(min=2, max=15, message='长度为2到15个字符'),
                    DataRequired(message='文章标题不能为空')],
        render_kw={"id": "article_title",
                   "class": "form-control",
                   "placeholder": "填写文章标题"}
    )

    article_img_url = StringField(
        label='标题图片url',
        validators=[Length(min=0, max=200, message='长度为0到200个字符')],
        render_kw={"id": "article_img_url",
                   "class": "form-control",
                   "placeholder": "填写标题图片url"}
    )


    article_desc = StringField(
        label='文章描述',
        validators=[Length(min=0, max=200, message='长度为0到200个字符')],
        render_kw={"id": "article_desc",
                   "class": "form-control",
                   "placeholder": "填写文章描述"}
    )


    see_power = SelectField(
        label='文章浏览权限',
        validators=[DataRequired(message='文章权限不能为空')],
        coerce=int,
        choices=[(power.id, power.name) for power in powers],
        render_kw={"id": "see_power",
                   "class": "form-control"}
    )

    article_tag = SelectField(
        label='文章类别',
        validators=[DataRequired(message='文章类别不能为空')],
        coerce=int,
        choices=[(article_tag.id, article_tag.name) for article_tag in article_tags],

        render_kw={"id": "article_tag",
                   "class": "form-control"}
    )


    article_text = TextAreaField(
            label='文章正文',
            validators=[Length(min=0, max=2000, message='最长为2000个字符')],
            render_kw={"id": "article_text",
                       "class": "ckeditor",
                       "placeholder": "填写正文"}
    )

    submit = SubmitField(
        label='开始提交',
        render_kw={"class": "btn btn-primary",
                   "value": "开始提交"}

    )



class AboutMsgForm(FlaskForm):
    about_msg = TextAreaField(
        label='留言',
        validators=[Length(min=1, max=100, message='长度为1到100个字符')],
        render_kw={"id": "about_msg",
                   "class": "form-control",
                   "placeholder": "填写内容"}
    )

    submit = SubmitField(
        label='开始提交',
        render_kw={"class": "btn btn-primary",
                   "value": "开始提交"}

    )

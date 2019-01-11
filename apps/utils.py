import os, uuid
from datetime import datetime
from PIL import Image

def exis_files(files_paths):
    #判断文件目录是否存在
    if not os.path.exists(files_paths):
        os.makedirs(files_paths)
        # os.chmod(files_paths, os.O_RDWR)提权报错


#修改文件名称
def change_filename_with_timestamp_uuid(filename):
    #分离文件名和扩展名，返回一个元组
    fileinfo = os.path.splitext(filename)
    nowTime = datetime.now().strftime('%Y%m%d%H%M%S')
    #与十六进制随机数进行拼接
    filename = str(nowTime) + str(uuid.uuid4().hex) + fileinfo[-1].lower()

    return filename

ALLOWED_IMAGE_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'bmp'])
ALLOWED_VIDEO_EXTENSIONS = set(['mp4', 'avi'])
ALLOWED_AUDIO_EXTENSIONS = set(['mp3', 'm4a'])

#检查文件后缀
def check_files_extension(filenamelist, allowed_extensions):
    for fname in filenamelist:
        check_fname = '.' in fname and \
            fname.rsplit('.', 1)[1].lower() in allowed_extensions
        if not check_fname:
            return False
    return True


def create_face(path, filename, base_width=200):
    imgname, ext = os.path.splitext(filename)#分离文件名与扩展名
    newfilename = imgname + '_face_' + ext   #缩略图文件名
    img = Image.open(os.path.join(path, filename)) #根据指定的路径打开图像
    #size[0]宽度 如果图片宽度大于base_width
    if img.size[0] > base_width:
        #设置百分比,调节其他部分
        w_percent = (base_width / float(img.size[0]))
        h_size = int((float(img.size[1]) * float(w_percent)))
        img = img.resize((base_width, h_size), Image.ANTIALIAS)
    img.save(os.path.join(path, newfilename))
    return newfilename




def create_thumbnail(path, filename, base_width=300):
    imgname, ext = os.path.splitext(filename)#分离文件名与扩展名
    newfilename = imgname + '_small_' + ext   #缩略图文件名
    img = Image.open(os.path.join(path, filename)) #根据指定的路径打开图像
    #size[0]宽度 如果图片宽度大于base_width
    if img.size[0] > base_width:
        #设置百分比,调节其他部分
        w_percent = (base_width / float(img.size[0]))
        h_size = int((float(img.size[1]) * float(w_percent)))
        img = img.resize((base_width, h_size), Image.ANTIALIAS)
    img.save(os.path.join(path, newfilename))
    return newfilename


def create_show(path, filename, base_width=800):
    imgname, ext = os.path.splitext(filename)#分离文件名与扩展名
    newfilename = imgname + '_show_' + ext   #缩略图文件名
    img = Image.open(os.path.join(path, filename)) #根据指定的路径打开图像
    #size[0]宽度 如果图片宽度大于base_width
    if img.size[0] > base_width:
        #设置百分比,调节其他部分
        w_percent = (base_width / float(img.size[0]))
        h_size = int((float(img.size[1]) * float(w_percent)))
        img = img.resize((base_width, h_size), Image.ANTIALIAS)
    img.save(os.path.join(path, newfilename))
    return newfilename
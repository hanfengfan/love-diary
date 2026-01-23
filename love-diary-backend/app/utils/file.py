import os
import uuid
from werkzeug.utils import secure_filename
from moviepy.editor import VideoFileClip
from PIL import Image

def save_uploaded_file(file, upload_folder, allowed_extensions):
    """保存上传的文件"""
    if file.filename == '':
        return None, "没有选择文件"

    if not allowed_file(file.filename, allowed_extensions):
        return None, "文件类型不允许"

    # 生成安全的文件名
    filename = secure_filename(file.filename)
    unique_filename = str(uuid.uuid4()) + '_' + filename
    filepath = os.path.join(upload_folder, unique_filename)

    # 确保目录存在
    os.makedirs(upload_folder, exist_ok=True)

    # 保存文件
    file.save(filepath)

    return unique_filename, None

def generate_video_thumbnail(video_path, thumbnail_path):
    """生成视频缩略图"""
    try:
        clip = VideoFileClip(video_path)
        frame = clip.get_frame(1)  # 获取第1秒的帧
        clip.close()

        # 保存为图片
        from PIL import Image
        img = Image.fromarray(frame)
        img.save(thumbnail_path)
        return True
    except Exception as e:
        print(f"生成缩略图失败: {e}")
        return False

def get_video_duration(video_path):
    """获取视频时长（秒）"""
    try:
        clip = VideoFileClip(video_path)
        duration = int(clip.duration)
        clip.close()
        return duration
    except Exception as e:
        print(f"获取视频时长失败: {e}")
        return 0
from turtle import right, width
import cv2
import numpy as np
import subprocess



device_id = "ea499ae7"   # 设备序列号

def capture_current_screen(device_id):
    """
    捕获设备的当前屏幕图像。

    参数:
    device_id: 目标设备的序列号。

    返回:
    当前屏幕图像的路径。
    """
    # 执行ADB命令以捕获屏幕图像
    screen_image_path = f"images/tests/{device_id}_current_screen.png"
    subprocess.run(["adb", "-s", device_id, "screencap", "-p", screen_image_path])
    return screen_image_path

def process_image(image_path):
    """
    调整图像大小和分辨率以适应模板匹配的需要。

    参数:
    image_path: 图像的路径。

    返回:
    处理后的图像路径。
    """
    # 读取图像
    image = cv2.imread(image_path)
    
    # 定义模板图片的分辨率
    desired_resolution = (2880, 1800)
    
    # 获取图像的原始尺寸
    original_height, original_width = image.shape[:2]
    
    # 检查图像分辨率是否需要调整
    if original_width != desired_resolution[0] or original_height != desired_resolution[1]:
        # 如果需要，调整图像大小到目标分辨率
        image = cv2.resize(image, desired_resolution)
        # 保存调整后的图像
        cv2.imwrite(image_path, image)
    
    return image_path

def match_template(template_path, image_path):
    """
    使用OpenCV的matchTemplate函数与参考图像（模板）进行匹配。

    参数:
    template_path: 参考图像（模板）的路径。
    image_path: 要搜索的图像的路径。

    返回:
    匹配结果的路径。
    """
    # 读取参考图像（模板）和要搜索的图像
    template = cv2.imread(template_path, 0)
    image = cv2.imread(image_path, 0)
    # 执行模板匹配
    result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
    # 存储匹配结果
    result_path = f"images/tests/{template_path.split('/')[-1].split('.')[0]}_match_result.png"
    cv2.imwrite(result_path, result)
    return result_path

def find_match(current_screen_path, template_paths, template_resolution):
    """
    使用图像识别模块找到匹配的图像。

    参数:
    current_screen_path: 当前屏幕图像的路径。
    template_paths: 参考图像（模板）的路径列表。
    template_resolution: 模板图像的分辨率。

    返回:
    匹配的参考图像（模板）的路径，如果未找到匹配的图像，则返回None。
    """
    # 处理当前屏幕图像，使其与模板图像的分辨率一致
    processed_screen_path = process_image(current_screen_path, desired_resolution=template_resolution)

    # 读取处理后的屏幕图像
    processed_screen = cv2.imread(processed_screen_path)

    # 初始化匹配结果变量
    best_match_template = None
    best_match_score = 0

    # 假设所有模板图片的分辨率都是 2880,1880
    template_resolution = (2880, 1800)

    # 获取当前屏幕图像的路径
    current_screen_path = capture_current_screen(device_id)

    # 提供模板图片的路径列表
    template_paths = ["images/references/ref1.png", "images/references/ref2.png"]

    # 调用 find_match 函数，并提供模板分辨率
    match_path = find_match(current_screen_path, template_paths, template_resolution)

    # 对每个模板进行匹配
    for template_path in template_paths:
        # 执行模板匹配
        result_path = match_template(template_path, processed_screen_path)
        
        # 读取匹配结果图像
        result_image = cv2.imread(result_path, cv2.IMREAD_GRAYSCALE)
        
        # 计算匹配结果的最大值作为匹配分数
        max_val = np.max(result_image)
        
        # 如果找到更高的匹配分数，更新最佳匹配模板和分数
        if max_val > best_match_score:
            best_match_score = max_val
            best_match_template = template_path

    # 如果找到了最佳匹配模板，返回它的路径
    if best_match_template:
        return best_match_template

    # 如果没有找到匹配的模板，返回None
    return None

def perform_action_based_on_match(match_path, device_id):
    """
    根据匹配结果执行相应的操作。

    参数:
    match_path: 匹配结果的路径。
    device_id: 目标设备的序列号。
    """
    # 分析匹配结果
    # 确定匹配的参考图像（模板）
    # 执行相应的操作（如点击图像、执行特定的测试步骤等）
    # ...
    pass

# 使用示例
# 捕获当前屏幕图像
current_screen_path = capture_current_screen(device_id)
# 找到匹配的参考图像（模板）
match_path = find_match(current_screen_path, ["images/references/ref1.png", "images/references/ref2.png"])
# 根据匹配结果执行操作
if match_path:
    perform_action_based_on_match(match_path, device_id)
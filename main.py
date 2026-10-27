import fitz  # PyMuPDF
from PIL import Image
import io
import os


def pdf_to_long_image(
    pdf_path,
    output_path="long_image.png",
    zoom=2.5,
    gap=0,
    background="white"
):
    """
    将多页 PDF 转换并纵向拼接为一张长图。

    Parameters
    ----------
    pdf_path : str
        PDF 文件路径
    output_path : str
        输出长图路径，建议保存为 PNG
    zoom : float
        PDF 渲染倍率。
        2.0 约等于 144 DPI
        2.5 约等于 180 DPI
        3.0 约等于 216 DPI
    gap : int
        每页图片之间的间隔像素
    background : str
        背景颜色，默认为白色
    """

    # 打开 PDF
    pdf = fitz.open(pdf_path)

    images = []

    # PDF 每页转图片
    for page_index in range(len(pdf)):
        page = pdf[page_index]

        matrix = fitz.Matrix(zoom, zoom)

        pix = page.get_pixmap(
            matrix=matrix,
            alpha=False
        )

        img = Image.open(
            io.BytesIO(pix.tobytes("png"))
        ).convert("RGB")

        images.append(img)

        print(
            f"已转换第 {page_index + 1}/{len(pdf)} 页："
            f"{img.width} × {img.height}"
        )

    pdf.close()

    if not images:
        raise ValueError("PDF 中没有页面。")

    # -----------------------------
    # 统一宽度
    # -----------------------------
    max_width = max(img.width for img in images)

    resized_images = []

    for img in images:
        if img.width != max_width:
            ratio = max_width / img.width

            new_height = int(img.height * ratio)

            img = img.resize(
                (max_width, new_height),
                Image.Resampling.LANCZOS
            )

        resized_images.append(img)

    # -----------------------------
    # 计算最终长图尺寸
    # -----------------------------
    total_height = (
        sum(img.height for img in resized_images)
        + gap * (len(resized_images) - 1)
    )

    long_image = Image.new(
        "RGB",
        (max_width, total_height),
        background
    )

    # -----------------------------
    # 纵向拼接
    # -----------------------------
    current_y = 0

    for img in resized_images:
        long_image.paste(
            img,
            (0, current_y)
        )

        current_y += img.height + gap

    # -----------------------------
    # 保存
    # -----------------------------
    os.makedirs(
        os.path.dirname(os.path.abspath(output_path)),
        exist_ok=True
    )

    long_image.save(
        output_path,
        quality=100
    )

    print("\n==============================")
    print("长图生成完成")
    print("输出路径：", os.path.abspath(output_path))
    print(
        "最终尺寸：",
        long_image.width,
        "×",
        long_image.height
    )
    print("==============================")


if __name__ == "__main__":

    PDF_PATH = r"C:\Users\18347\Desktop\照片\科研.pdf"

    OUTPUT_PATH = r"C:\Users\18347\Desktop\照片\科研.png"

    pdf_to_long_image(
        pdf_path=PDF_PATH,
        output_path=OUTPUT_PATH,

        # 清晰度
        zoom=2.5,

        # 页面之间不留缝
        gap=0
    )
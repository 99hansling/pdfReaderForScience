import re
import os
import PyPDF2
import tkinter as tk
from tkinter import filedialog

def extract_title(text):
    """
    提取论文标题（abstract之前的内容，除去作者名）
    :param text: PDF文本内容
    :return: 清理后的标题
    """
    # 打印前200个字符，查看文本提取情况
    print("\n提取的文本开头：")
    print("-" * 50)
    print(text[:200])
    print("-" * 50)
    
    # 查找 abstract 的位置（扩展匹配模式）
    abstract_patterns = [
        r'(?i)(abstract|摘要)\s*\n',
        r'(?i)abstract[:\-—]',
        r'(?i)\n\s*abstract\s*\n',
        r'(?i)^abstract\s*\n'
    ]
    
    abstract_match = None
    for pattern in abstract_patterns:
        match = re.search(pattern, text)
        if match:
            abstract_match = match
            print(f"找到 Abstract，使用模式: {pattern}")
            break
            
    if not abstract_match:
        print("未找到任何 Abstract 标记")
        return None
    
    # 获取 abstract 之前的文本
    title_text = text[:abstract_match.start()].strip()
    print("\n提取的标题部分：")
    print("-" * 50)
    print(title_text)
    print("-" * 50)
    
    # 清理标题文本
    def clean_title(title):
        # 按行分割
        lines = title.split('\n')
        title_lines = []
        is_title = True
        
        print("\n处理每一行：")
        print("-" * 50)
        
        for line in lines:
            line = line.strip()
            if not line:
                print("空行")
                is_title = False
                continue
            
            print(f"当前行: {line}")
            print(f"当前是否是标题部分: {is_title}")
            
            # 跳过作者行的特征
            skip_line = False
            
            # 如果是第一行或前面已有标题行，使用不同的规则
            if len(title_lines) == 0:  # 第一行
                skip_line = (
                    # 包含邮箱
                    '@' in line or 'email' in line.lower() or
                    # 包含机构关键词
                    any(word in line.lower() for word in ['university', 'institute', 'department', 'school', 'laboratory', 'lab', 'technologies']) or
                    # 明显是作者行（多个人名）
                    (len(re.findall(r'\b[A-Z][a-z]+\b', line)) > 1 and (',' in line or ' and ' in line.lower()))
                )
            else:  # 后续行
                skip_line = not is_title or (
                    # 包含多个逗号或and的行
                    (',' in line or ' and ' in line.lower()) or
                    # 包含邮箱
                    ('@' in line or 'email' in line.lower()) or
                    # 包含机构关键词
                    any(word in line.lower() for word in ['university', 'institute', 'department', 'school', 'laboratory', 'lab', 'technologies']) or
                    # 包含数字上标和特殊符号
                    bool(re.search(r'[\d\*\†\{\}]', line)) or
                    # 包含多个人名
                    len(re.findall(r'\b[A-Z][a-z]+\b', line)) > 1 or
                    # 以小写字母开头且不是明显的标题延续
                    (line[0].islower() and not any(word in line.lower() for word in ['with', 'for', 'of', 'and', 'in', 'on', 'to', 'by']))
                )
            
            if skip_line:
                is_title = False
                print(f"跳过原因: {'不是标题部分' if not is_title else '匹配到跳过规则'}")
            else:
                print("保留此行")
                title_lines.append(line)
        
        if not title_lines:
            print("警告：没有找到有效的标题行")
            return None
            
        # 合并标题行
        title = ' '.join(title_lines)
        
        # 清理特殊字符，但保留连字符
        title = re.sub(r'[^\w\s-]', '', title)
        # 替换多个空格为单个空格
        title = re.sub(r'\s+', ' ', title)
        # 限制长度
        title = title[:100] if len(title) > 100 else title
        
        print("\n清理后的标题：")
        print("-" * 50)
        print(title)
        print("-" * 50)
        
        return title.strip()
    
    return clean_title(title_text)

def read_pdf(file_path):
    """
    读取PDF文件并提取文本
    :param file_path: PDF文件路径
    :return: 提取的文本内容
    """
    with open(file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        text = pdf_reader.pages[0].extract_text()  # 只读取第一页
        return text

def select_files():
    """
    打开文件选择对话框��择多个PDF文件
    :return: 选择的文件路径列表
    """
    root = tk.Tk()
    root.withdraw()
    file_paths = filedialog.askopenfilenames(
        title="选择PDF文件",
        filetypes=[
            ("PDF文件", "*.pdf"),
            ("所有文件", "*.*")
        ]
    )
    return file_paths

def rename_pdf_files():
    """
    函数：选择PDF文件并根据标题重命名
    """
    print("请选择要重命名的PDF文件...")
    file_paths = select_files()
    
    if not file_paths:
        print("未选择文件")
        return
    
    for file_path in file_paths:
        try:
            # 读取PDF
            text = read_pdf(file_path)
            
            # 提取标题
            title = extract_title(text)
            if not title:
                print(f"无法从文件提取标题: {file_path}")
                continue
            
            # 生成新文件名
            dir_path = os.path.dirname(file_path)
            new_filename = f"{title}.pdf"
            new_filepath = os.path.join(dir_path, new_filename)
            
            # 确保文件名唯一
            counter = 1
            while os.path.exists(new_filepath):
                base_name = new_filename[:-4]  # 移除 .pdf
                new_filepath = os.path.join(dir_path, f"{base_name}_{counter}.pdf")
                counter += 1
            
            # 重命名文件
            os.rename(file_path, new_filepath)
            print(f"已重命名: {os.path.basename(file_path)} -> {os.path.basename(new_filepath)}")
            
        except Exception as e:
            print(f"处理文件时出错 {file_path}: {str(e)}")

if __name__ == "__main__":
    rename_pdf_files() 
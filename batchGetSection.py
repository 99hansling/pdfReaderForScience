import re
import tkinter as tk
from tkinter import filedialog
import PyPDF2

def clean_content(text):
    """
    清理文本内容：
    1. 去除多余的空格
    2. 合并多个换行
    3. 修复断行导致的单词分割
    :param text: 原始文本
    :return: 清理后的文本
    """
    # 去除多余的空格
    text = ' '.join(text.split())
    
    # 处理断行的单词（例如：word- ing -> wording）
    text = re.sub(r'(\w+)-\s*\n\s*(\w+)', r'\1\2', text)
    
    # 处理句子中的换行
    text = re.sub(r'(?<=[^.])\n(?=[a-zA-Z])', ' ', text)
    
    # 保留段落之间的换行（两个或更多换行）
    text = re.sub(r'\n\s*\n\s*', '\n\n', text)
    
    return text.strip()

def extract_sections(text):
    """
    提取文本中的特定章节内容（Abstract, Introduction, conclusions）
    :param text: 输入的文本内容
    :return: 包含各章节内容的字典
    """
    # 初始化结果字典
    sections = {
        'abstract': '',
        'introduction': '',
        'conclusions': ''
    }
    
    # 定义章节标题的正则模式
    patterns = {
        'abstract': r'(?i)(abstract|摘要)\s*\n',
        'introduction': r'(?i)(1\.?\s+)?(introduction|overview)\s*\n',  # 添加 overview 匹配
        'conclusions': r'(?i)(\d+[\.\s]+)?(conclusions?|结论)\s*\n'
    }
    
    # 定义数字编号章节的模式
    section_start_pattern = r'\n2\.'  # 直接匹配 "\n2."
    
    # 定义参考文献部分的模式
    references_pattern = r'\n[Rr]eferences?\s*\n'
    
    # 查找所有可能的章节标题位置
    section_positions = []
    for section, pattern in patterns.items():
        matches = list(re.finditer(pattern, text, re.IGNORECASE))
        for match in matches:
            section_positions.append((match.start(), section, match.group()))
    
    # 查找参考文献部分的位置
    references_match = re.search(references_pattern, text)
    references_pos = references_match.start() if references_match else len(text)
    
    # 查找第2节的开始位置
    section_2_match = re.search(section_start_pattern, text)
    section_2_pos = section_2_match.start() if section_2_match else len(text)
    
    # 按位置排序
    section_positions.sort()
    
    # 提取章节内容
    for i, (pos, section, title) in enumerate(section_positions):
        start = pos + len(title)
        
        # 获取结束位置
        if section == 'introduction':
            # introduction 章节到第2节开始
            end = section_2_pos
        elif i < len(section_positions) - 1:
            # 其他章节到下一个识别的章节位置结束
            next_section = section_positions[i + 1][0]
            end = next_section
        else:
            # 如果是最后一个章节，使用参考文献部分的位置作为结束点
            end = references_pos
        
        # 提取内容并清理
        content = text[start:end].strip()
        content = clean_content(content)  # 使用新的清理函数
        
        if section in sections:
            sections[section] = content
    
    return sections

def select_file():
    """
    打开文件选择对话框选择PDF文件
    :return: 选择的文件路径
    """
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口
    file_path = filedialog.askopenfilename(
        title="选择PDF文件",
        filetypes=[
            ("PDF文件", "*.pdf"),
            ("所有文件", "*.*")
        ]
    )
    return file_path

def read_file(file_path):
    """
    读取PDF文件并提取文本
    :param file_path: PDF文件路径
    :return: 提取的文本内容
    """
    with open(file_path, 'rb') as file:
        # 创建PDF读取器对象
        pdf_reader = PyPDF2.PdfReader(file)
        
        # 存储所有文本
        all_text = []
        
        # 遍历每一页并提取文本
        for page in pdf_reader.pages:
            text = page.extract_text()
            if text.strip():
                all_text.append(text.strip())
        
        # 合并所有页面的文本
        return '\n'.join(all_text)

def save_sections(sections, output_dir='.'):
    """
    将提取的章节内容保存到单独的文件
    :param sections: 章节内容字典
    :param output_dir: 输出目录
    """
    for section, content in sections.items():
        if content:  # 只保存非空章节
            file_path = f"{output_dir}/{section}.txt"
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)
            print(f"已保存 {section} 到 {file_path}")

def main():
    print("请选择要读取的文本文件...")
    file_path = select_file()
    
    if file_path:  # 如果用户选择了文件
        try:
            # 读取文件
            text = read_file(file_path)
            
            # 提取章节
            sections = extract_sections(text)
            
            # 打印提取结果
            for section, content in sections.items():
                if content:
                    print(f"\n{section.upper()}:")
                    print("-" * 50)
                    # 只打印前200个字符
                    preview = content[:200] + "..." if len(content) > 200 else content
                    print(preview)
                    print("-" * 50)
                else:
                    print(f"\n未找到 {section} 章节")
            
            # 询问是否保存到文件
            save = input("\n是否将章节内容保存到单独的文件？(y/n): ")
            if save.lower() == 'y':
                save_sections(sections)
                
        except Exception as e:
            print(f"发生错误：{str(e)}")
    else:
        print("未选择文件")

if __name__ == "__main__":
    main() 
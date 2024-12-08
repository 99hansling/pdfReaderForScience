import re
import os
import PyPDF2
import tkinter as tk
from tkinter import filedialog

def read_pdf(file_path):
    """
    读取PDF文件并提取文本
    :param file_path: PDF文件路径
    :return: 提取的文本内容
    """
    with open(file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        all_text = []
        for page in pdf_reader.pages:
            text = page.extract_text()
            if text.strip():
                all_text.append(text.strip())
        return '\n'.join(all_text)

def extract_references(text):
    """
    从文本中提取参考文献部分
    :param text: 完整文本
    :return: 参考文献文本
    """
    # 查找参考文献部分的更多模式
    ref_patterns = [
        r'\n[Rr][Ee][Ff][Ee][Rr][Ee][Nn][Cc][Ee][Ss]\s*\n',  # 完全匹配 REFERENCES
        r'\n[Rr]eferences?\s*\n',
        r'\nBibliography\s*\n',
        r'\n参考文献\s*\n',
        r'\n[Rr]eferences?[:\-—]',
        r'\n[Rr]eferences?\s+',
        r'(?i)\[\s*references?\s*\]',
        r'\d+\.\s+[Rr]eferences?\s*\n',
        r'\n[Rr]eferences?\s+cited\s*\n',
        r'\nWorks [Cc]ited\s*\n',
        r'\nLiterature [Cc]ited\s*\n'
    ]
    
    # 打印前200个字符，帮助调试
    print("\n文本开头：")
    print("-" * 50)
    print(text[:200])
    print("-" * 50)
    
    ref_start = None
    matched_pattern = None
    
    for pattern in ref_patterns:
        match = re.search(pattern, text)
        if match:
            ref_start = match.end()
            matched_pattern = pattern
            print(f"找到参考文献部分，使用模式: {pattern}")
            break
    
    if ref_start is None:
        print("\n未找到参考文献部分。尝试查找的模式：")
        for pattern in ref_patterns:
            print(f"- {pattern}")
        return None
        
    # 提取参考文献部分的文本
    ref_text = text[ref_start:].strip()
    
    # 处理换行和连字符问题
    ref_text = re.sub(r'-\s*\n\s*', '', ref_text)  # 移除行尾连字符
    ref_text = re.sub(r'(?<=[^.])\n(?=[a-z])', ' ', ref_text)  # 合并被换行分割的句子
    
    # 打印参考文献部分的前200个字符，帮助调试
    print("\n提取的参考文献开头：")
    print("-" * 50)
    print(ref_text[:200])
    print("-" * 50)
    
    return ref_text

def parse_references(ref_text):
    """
    解析参考文献，返回编号到引用的映射
    :param ref_text: 参考文献文本
    :return: 引用字典
    """
    # 匹配参考文献条目的更多模式
    ref_patterns = [
        # [1] 标准格式，考虑多行
        r'\[(\d+)\](.*?)(?=\[\d+\]|\Z)',
        # [1] 格式但考虑可能的换行
        r'(?s)\[(\d+)\](.*?)(?=\s*\[\d+\]|\Z)',
        # 1. 格式
        r'(?m)^(\d+)\.(.*?)(?=^\d+\.|\Z)',
        # [ABC20] 格式
        r'\[([A-Za-z0-9]+)\](.*?)(?=\[[A-Za-z0-9]+\]|\Z)',
        # (1) 格式
        r'\((\d+)\)(.*?)(?=\(\d+\)|\Z)',
        # 简单的数字开头
        r'(?m)^(\d+)[\.|\s](.*?)(?=^\d+[\.|\s]|\Z)'
    ]
    
    references = {}
    matched_pattern = None
    
    for pattern in ref_patterns:
        matches = list(re.finditer(pattern, ref_text, re.DOTALL))
        if matches:
            matched_pattern = pattern
            print(f"使用引用匹配模式: {pattern}")
            for match in matches:
                ref_num = match.group(1)
                ref_content = match.group(2).strip()
                # 清理引用内容
                ref_content = re.sub(r'\s+', ' ', ref_content)  # 规范化空白
                if ref_content:  # 只添加非空引用
                    references[ref_num] = ref_content
            break
    
    if not references:
        print("\n未找到参考文献条目。尝试查找的模式：")
        for pattern in ref_patterns:
            print(f"- {pattern}")
    else:
        print(f"\n找到 {len(references)} 个参考文献条目")
        # 打印前三个条目作为示例
        print("\n示例条目：")
        for i, (num, content) in enumerate(list(references.items())[:3]):
            print(f"[{num}] {content[:100]}...")
    
    return references

def extract_selected_references():
    """
    主函数：选择PDF文件并提取指定的参考文献
    """
    # 选择PDF文件
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="选择PDF文件",
        filetypes=[("PDF文件", "*.pdf")]
    )
    
    if not file_path:
        print("未选择文件")
        return
    
    try:
        # 读取PDF
        print("正在读取PDF文件...")
        text = read_pdf(file_path)
        
        # 提取参考文献部分
        print("正在提取参考文献部分...")
        ref_text = extract_references(text)
        if not ref_text:
            print("未找到参考文献部分")
            return
            
        # 解析所有参考文献
        print("正在解析参考文献...")
        references = parse_references(ref_text)
        if not references:
            print("未找到任何参考文献条目")
            return
            
        # 获取用户输入的引用号
        print("\n请输入要提取的引用编号（用逗号分隔，例如：1,3,5-7）：")
        ref_nums_input = input().strip()
        
        # 解析引用号范围
        selected_refs = set()
        for part in ref_nums_input.split(','):
            if '-' in part:
                start, end = map(str.strip, part.split('-'))
                # 处理数字引用
                if start.isdigit() and end.isdigit():
                    selected_refs.update(map(str, range(int(start), int(end) + 1)))
                else:
                    selected_refs.add(start)
                    selected_refs.add(end)
            else:
                selected_refs.add(part.strip())
        
        # 创建输出文件
        output_dir = os.path.dirname(file_path)
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        output_path = os.path.join(output_dir, f"{base_name}_references.txt")
        
        # 写入选定的参考文献
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"从文件 {os.path.basename(file_path)} 中提取的参考文献：\n")
            f.write("=" * 50 + "\n\n")
            
            for ref_num in sorted(selected_refs, key=lambda x: (len(x), x)):
                if ref_num in references:
                    f.write(f"[{ref_num}] {references[ref_num]}\n\n")
                else:
                    print(f"警告：未找到引用编号 [{ref_num}]")
        
        print(f"\n已将选定的参考文献保存到：{output_path}")
        
    except Exception as e:
        print(f"处理文件时出错: {str(e)}")

if __name__ == "__main__":
    extract_selected_references() 
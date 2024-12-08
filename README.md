# Academic Paper Section Extractor & Reference Processor

# 学术论文章节提取与引用处理工具

A tool suite for extracting sections from academic papers and processing citations.
一套用于提取学术论文章节并处理引用的工具套件。

## Features / 功能特点

- Extract abstract, introduction, and conclusions from PDF papers
- Process citations in Word documents
- Batch processing support
- Rename files based on titles
- 从PDF论文中提取摘要、引言和结论
- 处理Word文档中的引用
- 支持批量处理
- 基于标题重命名文件

## File Structure / 文件结构

### Main Processing Scripts / 主要处理脚本

- `process_word_citations.py`: Process citations in Word documents, converting them to a numbered format
  处理Word文档中的引用，将其转换为编号格式
- `extract_references.py`: Extract references from PDF papers
  从PDF论文中提取参考文献
- `batchGetSection.py`: Extract specific sections (abstract, introduction, conclusions) from PDF papers
  从PDF论文中提取特定章节（摘要、引言、结论）
- `rename_by_title.py`: Rename PDF files based on their titles
  根据论文标题重命名PDF文件

### Batch Processing / 批处理

- `batch_extract_to_word.py`: Batch process multiple PDF files and export to Word
  批量处理多个PDF文件并导出为Word格式

### Testing / 测试

- `cursortest.py`: Test script for cursor operations
  光标操作测试脚本

### Output Files / 输出文件

- `abstract.txt`: Extracted abstracts
  提取的摘要
- `introduction.txt`: Extracted introductions
  提取的引言
- `conclusions.txt`: Extracted conclusions
  提取的结论

## Usage / 使用方法

### Citation Processing / 引用处理

`python batchGetSection.py`

Extract sections from PDF papers:
从 PDF 论文中提取章节：

1. Select one or multiple PDF files
   选择一个或多个 PDF 文件
2. The script extracts:
   脚本将提取：
   - Abstract / 摘要
   - Introduction / 引言
   - Conclusions / 结论
3. Results are saved to separate .txt files
   结果保存到单独的 .txt 文件中

### Batch Processing / 批量处理

```bash
python batch_extract_to_word.py
```

Process multiple papers at once:
一次处理多篇论文：

1. Select a folder containing PDF files
   选择包含 PDF 文件的文件夹
2. The script will:
   脚本将会：
   - Extract sections from all papers
     从所有论文中提取章节
   - Combine them into a single Word document
     将它们合并到一个 Word 文档中
   - Maintain proper formatting
     保持适当的格式

### File Renaming / 文件重命名

```bash
python rename_by_title.py
```

Rename PDF files based on their titles:
根据论文标题重命名 PDF 文件：

1. Select PDF files to rename
   选择要重命名的 PDF 文件
2. The script extracts the title and renames the file
   脚本提取标题并重命名文件

## Requirements / 依赖要求

```bash
pip install -r requirements.txt
```

Required packages / 所需包：
- python-docx >= 0.8.11
- PyPDF2 >= 3.0.0
- tkinter (usually comes with Python)
- pdfplumber >= 0.7.0
- python-docx >= 0.8.11

## Project Structure / 项目结构

```
.
├── process_word_citations.py   # Citation processor / 引用处理器
├── batchGetSection.py         # Section extractor / 章节提取器
├── batch_extract_to_word.py   # Batch processor / 批处理器
├── rename_by_title.py         # File renamer / 文件重命名器
├── extract_references.py      # Reference extractor / 参考文献提取器
├── cursortest.py             # Test script / 测试脚本
├── requirements.txt          # Dependencies / 依赖项
└── test/                     # Test files / 测试文件
    ├── test.docx
    └── test.pdf
```

## Common Issues / 常见问题

1. PDF Not Readable / PDF 不可读
   - Ensure PDFs are searchable text, not scanned images
     确保 PDF 是可搜索的文本，而不是扫描图片
   - Convert scanned PDFs using OCR first
     先对扫描的 PDF 进行 OCR 转换

2. Citation Format / 引用格式
   - Citations must be enclosed in 【】
     引用必须用【】括起来
   - Ensure proper formatting in Word documents
     确保 Word 文档中的格式正确

## Contributing / 贡献

1. Fork the repository
   复刻仓库
2. Create your feature branch
   创建特性分支
3. Commit your changes
   提交更改
4. Push to the branch
   推送到分支
5. Create a Pull Request
   创建拉取请求

## License / 许可证

This project is licensed under the MIT License - see the LICENSE file for details.
本项目采用 MIT 许可证 - 详见 LICENSE 文件。

## Acknowledgments / 致谢

- Thanks to all contributors
  感谢所有贡献者
- Special thanks to the open source community
  特别感谢开源社区

## Contact / 联系方式

For any questions or suggestions, please open an issue on GitHub.
如有任何问题或建议，请在 GitHub 上开启一个 issue。
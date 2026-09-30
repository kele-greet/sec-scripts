# sec-scripts

个人网络安全工具集（手写实现）  
本仓库记录我在网络安全学习过程中，**脱离 AI 手写**实现的基础安全工具与脚本，主要用于授权环境下的渗透测试练习、漏洞验证与自动化信息收集。

---

## 📁 目录结构

```
sec-scripts/
├── port_scanner.py          # Day01：多线程端口扫描
├── dir_brute.py             # Day01：目录爆破
├── log_parser.py            # Day01：日志解析与统计
├── exp01_mutability.py      # Day01：可变性与引用实验
├── exp02_containers.py      # Day01：容器类型实验
├── exp03_functions.py       # Day01：函数与闭包实验
├── exp04_decorator.py       # Day01：装饰器实验
├── exp05_classes.py         # Day01：类与继承实验
├── exp06_exceptions_io.py   # Day01：异常与文件 IO 实验
├── exp07_generators.py      # Day01：生成器实验
├── exp08_stdlib.py          # Day01：标准库实验
├── exp09_requests_bs4.py    # Day01：requests + BeautifulSoup 实验
├── access.log               # 示例日志
├── demo.log                 # 示例日志
├── words.txt                # 目录爆破字典
├── findings.json            # 扫描结果输出示例
├── out/                     # 输出目录
└── day02/                   # Day02：网络编程与协议深挖
    ├── tcp_probe.py         # TCP 连接探测
    ├── http_raw.py          # socket 手发原始 HTTP 请求
    ├── raw_variants.py      # 原始请求变体实验
    ├── subdomain_brute.py   # 子域名爆破 + 存活探测
    ├── encode_lab.py        # URL/HTML/Base64 编码实验
    └── jwt_peek.py          # JWT 结构解析与安全观察
```

---

## 🔧 Day01 · Python 手写地基

| 文件              | 功能                                                         | 用法示例                                           |
| ----------------- | ------------------------------------------------------------ | -------------------------------------------------- |
| `port_scanner.py` | 多线程端口扫描，支持超时与端口范围                           | `python port_scanner.py 127.0.0.1 1-1024`          |
| `dir_brute.py`    | 目录爆破，支持状态码过滤与结果去重                           | `python dir_brute.py http://example.com words.txt` |
| `log_parser.py`   | 日志解析，统计攻击 IP Top N 与状态码分布                     | `python log_parser.py access.log`                  |
| `exp01~exp09`     | Python 语法手写实验（可变性、容器、函数、装饰器、类、异常、生成器、标准库、requests） | 直接运行，查看输出                                 |

---

## 🌐 Day02 · 网络编程与协议深挖

| 文件                 | 功能                                       | 用法示例                                |
| -------------------- | ------------------------------------------ | --------------------------------------- |
| `tcp_probe.py`       | TCP 连接探测，理解三次握手                 | `python tcp_probe.py 127.0.0.1 80`      |
| `http_raw.py`        | 用 socket 手发原始 HTTP 请求，理解报文结构 | `python http_raw.py 127.0.0.1 80`       |
| `raw_variants.py`    | 原始请求变体实验（方法/Header 修改）       | `python raw_variants.py`                |
| `subdomain_brute.py` | 子域名爆破 + HTTP 存活 + 标题提取          | `python subdomain_brute.py example.com` |
| `encode_lab.py`      | URL/HTML/Unicode/Base64 编码实验           | `python encode_lab.py`                  |
| `jwt_peek.py`        | JWT 结构解析与安全观察                     | `python jwt_peek.py <token>`            |

---

## ⚙️ 环境要求

- Python 3.10.12
- 依赖库：
  ```bash
  pip install requests beautifulsoup4
  ```
- 标准库：`socket`、`threading`、`concurrent.futures`、`re`、`argparse`、`logging`、`json`、`base64` 等。

---

## 🚀 快速开始

```bash
git clone https://github.com/kele-greet/sec-scripts.git
cd sec-scripts
pip install requests beautifulsoup4

# 运行端口扫描
python port_scanner.py 127.0.0.1 1-1024

# 运行目录爆破
python dir_brute.py http://example.com words.txt

# 运行日志解析
python log_parser.py access.log
```

---

## 📌 说明

- 所有脚本均为**手写实现**，用于锻炼底层编程与安全工具开发能力。
- 代码注释为中文，便于理解逻辑。
- 部分脚本仍在完善中，欢迎提交 Issue 或 PR。

---

## ⚠️ 免责声明

本仓库所有工具仅限**授权安全测试、学习研究**使用。  
严禁用于任何未授权的渗透测试、扫描或攻击行为。  
使用者需自行承担因不当使用产生的一切法律责任。

---

## 📫 联系

- GitHub: [kele-greet](https://github.com/kele-greet)

---

*如果这个仓库对你有帮助，欢迎 Star ⭐*
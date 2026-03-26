# 详细安装教程

## 方式一：Claude Code（推荐）

### 1. 安装 Claude Code

```bash
npm install -g @anthropic-ai/claude-code
```

### 2. 克隆仓库

```bash
git clone https://github.com/open-behavior-analysis/aba-clinical-agent.git
cd aba-clinical-agent
```

### 3. 配置权限

```bash
cp .claude/settings.local.json.example .claude/settings.local.json
```

编辑 `.claude/settings.local.json`，根据你的环境调整：
- 如果需要使用 `obsidian-cli`，确保 Obsidian 已安装并运行
- 如果需要 Python 数据分析功能，确保 Python 3.8+ 已安装

### 4. 启动

```bash
claude
```

在对话中输入你的第一条指令即可。

### 5. 可选：安装 Obsidian

1. 下载 [Obsidian](https://obsidian.md/)
2. 打开 Vault：选择 `Obsidian-Vault/` 目录
3. 安装推荐插件：Dataview、Calendar、Templater

## 方式二：Cursor / Cline

1. 克隆仓库
2. 用 Cursor 打开项目根目录
3. 在 AI 对话中输入指令

## 方式三：手动配置

如果你使用其他支持文件访问的 AI 客户端：
1. 确保客户端能读取 `.claude/skills/` 目录
2. 在系统提示中引入 `CLAUDE.md` 的内容
3. 确保客户端有文件读写权限

## 数据分析脚本依赖

```bash
pip install pandas openpyxl pdfplumber
```

## 首次使用建议

1. 先浏览示范个案 `Client-Demo-小星` 了解系统输出格式
2. 尝试 `quick-summary` 查看小星的全库摘要
3. 尝试 `intake-interview` 创建你的第一个个案

# Skill 开发者指南

## 什么是 Skill？

一个 Skill 是一个 `SKILL.md` 文件，定义了一个自动化临床任务的完整执行流程。它包含：

- **安全协议**：数据操作的约束和确认规则
- **输入规范**：需要什么用户输入和系统数据
- **执行步骤**：逐步的操作指令
- **输出规范**：生成什么文件、编辑什么文件、追加什么内容
- **下游建议**：执行完后推荐的下一步操作

## 创建新 Skill

### 1. 使用 skill-creator

最简单的方式是使用内置的 `skill-creator` 工具：

```
请帮我创建一个新的 Skill，用于 [描述你的需求]
```

### 2. 手动创建

在 `.claude/skills/` 下创建新目录和 `SKILL.md`：

```
.claude/skills/your-skill-name/
└── SKILL.md
```

### SKILL.md 标准结构

```markdown
---
name: your-skill-name
description: 一句话描述，用于路由匹配
---

## 安全协议
1. 数据敬畏：引用真实数据，不编造
2. 变更日志：所有文件操作记录到系统变更日志
3. [根据需要添加：预览确认、frontmatter更新等]

## 输入
[描述需要的用户输入和系统数据]

## 执行步骤
### Step 1: Read（读取数据）
### Step 2: Think（分析推理）
### Step 3: Write（生成输出）
### Step 4: Verify（验证完整性）

## 输出
[描述生成的文件列表]
```

### 3. 注册到路由

在 `_router.md` 中添加你的 Skill 的触发关键词映射。

### 4. 测试

使用虚构数据（如 Client-Demo-小星）测试你的 Skill。确保：
- 所有文件路径符合 `_config.md` 规范
- frontmatter 完整
- 双链正确
- 变更日志自动追加

## 最佳实践

- 遵循单一职责原则：一个 Skill 做一件事
- 在 Step 1 中充分读取上下文，避免后续步骤数据不足
- 使用 `> [!NOTE]` callout 展示预览
- 在输出末尾推荐下游 Skill

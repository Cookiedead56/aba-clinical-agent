#!/usr/bin/env python3
"""Translate all English vault files - replace remaining Chinese with English."""
import os
import re

BASE = "D:/OneDrive/wxob/aba-clinical-agent/i18n/en/vault"

# Comprehensive Chinese-to-English replacement pairs
REPLACEMENTS = [
    # Frontmatter
    ("tags: [个案]", "tags: [case]"),
    ("tags: [初访]", "tags: [intake]"),
    ("tags: [评估]", "tags: [assessment]"),
    ("tags: [教师]", "tags: [staff]"),
    ("tags: [沟通, 家书]", "tags: [communication, family-letter]"),
    ("tags: [数据/脱敏/原始记录]", "tags: [data/de-identified/raw-record]"),
    ("status: 🟠 方案执行中", 'status: "🟠 Plan in Progress"'),
    ("status: 🟢 激活", 'status: "🟢 Active"'),
    ("[待分配]", "[To be assigned]"),

    # Section headers
    ("### 📊 基线数据汇总", "### 📊 Baseline Data Summary"),
    ("### 👤 基本背景与病历摘要", "### 👤 Background & Medical History"),
    ("### 🧸 reinforcer偏好清单", "### 🧸 Reinforcer Preference List"),
    ("### 🧸 强化物偏好清单", "### 🧸 Reinforcer Preference List"),
    ("### 🧩 核心能力画像", "### 🧩 Core Skill Profile"),
    ("### 🚨 历史问题行为备忘", "### 🚨 Problem Behavior History"),
    ("### 📋 当前干预目标索引", "### 📋 Current Intervention Goals Index"),
    ("### 🔗 全生命周期索引", "### 🔗 Lifecycle Index"),
    ("## 🔗 关联文件", "## 🔗 Related Files"),

    # Common Chinese phrases in content
    ("**评估工具**", "**Assessment Tool**"),
    ("**评估日期**", "**Assessment Date**"),
    ("**评估详情**", "**Assessment Details**"),
    ("**最近评估日期**", "**Last Assessment Date**"),
    ("**儿童代号**", "**Child Code**"),
    ("**出生日期**", "**Date of Birth**"),
    ("**性别**", "**Gender**"),
    ("**当前年龄**", "**Current Age**"),
    ("**诊断**", "**Diagnosis**"),
    ("**确诊日期**", "**Diagnosis Date**"),
    ("**确诊机构**", "**Diagnosing Facility**"),
    ("**当前用药**", "**Current Medications**"),
    ("**入档日期**", "**Intake Date**"),
    ("**负责教师**", "**Assigned Therapist**"),
    ("**督导**", "**Supervisor**"),
    ("**初访日期**", "**Intake Date**"),
    ("**信息采集人**", "**Interviewer**"),
    ("**信息来源**", "**Information Source**"),
    ("**关联脱敏源**", "**Linked De-identified Source**"),
    ("**访谈日期**", "**Interview Date**"),

    # Table headers and content
    ("| 项目 | 内容 |", "| Item | Content |"),
    ("| 模块 | 得分 | 满分 | 百分比 | 阶段定位 |", "| Module | Score | Max | Percentage | Level |"),
    ("| 等级 | reinforcer | 效力评分 | 饱和度预警 | 适用场景 |", "| Tier | Reinforcer | Effectiveness | Satiation Risk | Use Case |"),
    ("| 领域 | 得分 | 表现描述 |", "| Domain | Score | Performance Description |"),
    ("| 编号 | 领域 | 学期目标 |", "| # | Domain | Semester Goal |"),
    ("| 编号 | 目标 | 基线 | 当前 | 月目标 | 状态 |", "| # | Goal | Baseline | Current | Monthly Target | Status |"),
    ("| 观察维度 | 基线表现 | 备注 |", "| Observation | Baseline | Notes |"),
    ("| 观察维度 | 基线表现 |", "| Observation | Baseline |"),
    ("| 行为 | 频率 | 初判功能 |", "| Behavior | Frequency | Hypothesized Function |"),
    ("| 等级 | reinforcer | 接近行为 | 持续时间 | 备注 |", "| Tier | Reinforcer | Approach Behavior | Duration | Notes |"),
    ("| 里程碑 | 实际月龄 | 典型月龄 | 备注 |", "| Milestone | Actual Age | Typical Age | Notes |"),
    ("| 时间段 | 机构/形式 | 频率 | 效果评价 |", "| Period | Provider/Type | Frequency | Outcome |"),
    ("| 优先级 | 痛点 | 家长描述 | 临床初判 |", "| Priority | Pain Point | Parent Description | Clinical Assessment |"),

    # Status values
    ("执行中", "In Progress"),
    ("杀手锏", "Top Tier"),
    ("储备", "Reserve"),
    ("待测试", "To Test"),
    ("待评估", "To Assess"),

    # Clinical terms
    ("核心发现摘要", "Key Findings Summary"),
    ("病历摘要", "Medical History Summary"),
    ("优势领域（可作为教学支架）", "Strengths (Can serve as instructional scaffolding)"),
    ("瓶颈领域（需密集干预）", "Deficit Areas (Require intensive intervention)"),
    ("长期目标（学期）", "Long-term Goals (Semester)"),
    ("短期目标（当前执行）", "Short-term Goals (Currently Active)"),
    ("社交回避行为（主要靶行为）", "Social Avoidance Behavior (Primary Target)"),
    ("集体活动中发出尖声", "Vocalization During Group Activities"),
    ("任务逃避（推开材料）", "Task Avoidance (Pushing Materials Away)"),
    ("操作定义", "Operational Definition"),
    ("功能假设", "Function Hypothesis"),
    ("基线频率", "Baseline Frequency"),
    ("干预策略", "Intervention Strategy"),
    ("社交互动", "Social Interaction"),
    ("集体参与", "Group Participation"),
    ("语言表达", "Language Expression"),
    ("行为管理", "Behavior Management"),
    ("个别化方案 v1", "Individualized Plan v1"),
    ("家书档案", "Family Letter Archive"),

    # Section titles in various files
    ("## 一、基本信息", "## 1. Basic Information"),
    ("## 二、发育史", "## 2. Developmental History"),
    ("## 三、家庭信息", "## 3. Family Information"),
    ("## 四、Top 3 痛点（家长视角 + 临床确认）", "## 4. Top 3 Pain Points (Parent + Clinical)"),
    ("## 五、基线行为观察（初访当日 + 前两次到访观察）", "## 5. Baseline Behavioral Observation"),
    ("## 六、reinforcer初筛", "## 6. Initial Reinforcer Screening"),
    ("## 七、已确认干预目标方向（4个维度）", "## 7. Confirmed Intervention Target Areas (4 Dimensions)"),
    ("### 1. 早期发育里程碑", "### 1. Early Developmental Milestones"),
    ("### 2. 诊断历程", "### 2. Diagnostic History"),
    ("### 3. 既往干预史", "### 3. Intervention History"),
    ("### 1. 家庭结构", "### 1. Family Structure"),
    ("### 2. 家庭generalization资源评估", "### 2. Family Generalization Resource Assessment"),
    ("### 3. 家长期望（妈妈原话摘录）", "### 3. Parent Expectations (Mother's Own Words)"),
    ("### 1. 语言与沟通", "### 1. Language & Communication"),
    ("### 2. 社交与游戏", "### 2. Social & Play"),
    ("### 3. 问题行为初筛", "### 3. Problem Behavior Screening"),
    ("### 观察法 + 妈妈报告", "### Observation + Mother's Report"),

    # Common words/phrases
    ("男", "Male"),
    ("无", "None"),
    ("略迟", "Slightly delayed"),
    ("显著延迟", "Significantly delayed"),
    ("严重延迟", "Severely delayed"),
    ("延迟", "Delayed"),
    ("至今未稳定出现", "Not yet consistently present"),
    ("语言发育迟缓", "Speech-Language Delay"),
    ("逃避", "Escape"),
    ("注意力获取", "Attention seeking"),
    ("自动reinforcement成分", "automatic reinforcement component"),
    ("reinforcement效力", "reinforcement effectiveness"),
    ("Motivating Operation (MO)（MO）", "Motivating Operation (MO)"),
    ("antecedent manipulation", "antecedent manipulation"),
    ("generalization", "generalization"),
    ("reinforcement", "reinforcement"),
    ("reinforcer", "reinforcer"),
    ("个案管理", "Case Management"),

    # Remaining isolated Chinese
    ("4岁2个月（入档时）", "4 years 2 months (at intake)"),
    ("4岁2个月", "4 years 2 months"),
    ("妈妈（主要养育者）", "Mother (primary caregiver)"),
    ("妈妈（手机：[已脱敏]）", "Mother (phone: [de-identified])"),
    ("全职照顾Alex，积极配合干预，愿意学习家庭generalization技术", "Full-time caregiver for Alex, actively cooperates with intervention, willing to learn home generalization techniques"),
    ("工作繁忙，参与度低，对ABA了解有限，态度为\"交给专业人员\"", 'Busy with work, low involvement, limited ABA knowledge, attitude of "leave it to professionals"'),
    ("偶尔帮忙带娃，溺爱倾向，常在Alex哭闹时立即满足需求", "Occasionally helps with childcare, tendency to indulge, often immediately satisfies demands when Alex cries"),
    ("中等", "Moderate"),
    ("总体评级", "Overall Rating"),
    ("妈妈学习意愿强，家中有独立训练空间，经济条件可支撑密集干预", "Mother has strong learning motivation, home has dedicated training space, financial conditions can support intensive intervention"),
    ("爸爸参与不足，祖父母的即时满足模式可能削弱延迟reinforcement的效果", "Father's insufficient involvement, grandparents' immediate gratification pattern may undermine delayed reinforcement effectiveness"),
    ("优势", "Strengths"),
    ("挑战", "Challenges"),
    ("社交互动技能缺乏 + 可能存在逃避功能", "Lack of social interaction skills + possible escape function"),
    ("听者反应弱、联合注意力不足", "Weak listener responding, insufficient joint attention"),
    ("Mand以单词+手势引导为主，需拓展句式长度", "Mand primarily single-word + gesture-guided, needs sentence length expansion"),
    ("社交发起困难", "Difficulty initiating social interactions"),
    ("集体指令回应差", "Poor group instruction compliance"),
    ("语言表达单一", "Limited expressive language"),
    ("从来不主动找小朋友，别人靠近他就跑开", "Never initiates with peers, runs away when others approach"),
    ("老师叫全班坐下他完全没反应", "No response when teacher tells the whole class to sit down"),
    ("只会说单个词，要什么东西就拉我的手", "Can only say single words, pulls my hand when he wants something"),
    ("逃避社交互动的高难度要求", "Escape from high-demand social interaction requirements"),
    ("疑似注意力获取或自我刺激", "Suspected attention-seeking or self-stimulation"),
    ("逃避非偏好任务", "Escape from non-preferred tasks"),
    ("高频：集体活动时几乎每次", "High frequency: almost every group activity"),
    ("中频：每次集体活动约2-3次", "Medium frequency: approximately 2-3 times per group activity"),
    ("中频：非偏好活动中", "Medium frequency: during non-preferred activities"),
    ("动机最强", "Strongest motivation"),
    ("可用于社交诱发", "Can be used for social elicitation"),
    ("可用作活动间reinforcement", "Can be used as between-activity reinforcement"),
    ("可用于大运动环节", "Can be used for gross motor activities"),
    ("需正式MSWO评估", "Needs formal MSWO assessment"),
    ("社交负reinforcement", "social negative reinforcement"),
    ("差别reinforcement（DRA）", "differential reinforcement (DRA)"),
    ("汽车玩具（小赛车）", "Toy cars (small race cars)"),
    ("泡泡", "Bubbles"),
    ("音乐歌曲（《Alex星》等）", 'Music/songs ("Twinkle Star" etc.)'),
    ("跳跳球", "Bouncing ball"),
    ("贴纸", "Stickers"),
    ("立即抓取、反复旋转车轮", "Immediately grabs, repeatedly spins wheels"),
    ("追逐、注视、尝试戳破", "Chases, watches, tries to pop"),
    ("身体摇晃、微笑", "Body rocking, smiling"),
    ("追逐、拍打", "Chases, pats"),
    ("未观察到明显偏好", "No clear preference observed"),
    ("代币系统候选", "Token economy candidate"),
    ("大运动环节、课间休息", "Gross motor activities, breaks"),
    ("活动间过渡、情绪调节", "Activity transitions, emotional regulation"),
    ("社交互动诱发、NET自然情境", "Social interaction elicitation, NET natural environment"),
    ("DTT高难度试次、新技能塑形", "DTT high-demand trials, new skill shaping"),
    ("汽车玩具（尤其小赛车）", "Toy cars (especially small race cars)"),
    ("独坐", "Independent sitting"),
    ("独走", "Independent walking"),
    ("首个有意义词汇", "First meaningful word"),
    ("两词句组合", "Two-word combinations"),
    ("指向性手势", "Pointing gestures"),
    ("7个月", "7 months"),
    ("14个月", "14 months"),
    ("22个月", "22 months"),
    ("20个月", "20 months"),
    ("6个月", "6 months"),
    ("12个月", "12 months"),
    ("24个月", "24 months"),
    ("9-12个月", "9-12 months"),
    ("妈妈", "Mother"),
    ("爸爸", "Father"),
    ("祖父母", "Grandparents"),
    ("平行游戏为主，无发起、无回应，同伴靠近时有时会移开", "Primarily parallel play, no initiation, no response, sometimes moves away when peers approach"),
    ("功能性游戏（推车、搭积木），无假想游戏", "Functional play (pushing cars, building blocks), no pretend play"),
    ("极少主动展示或分享，偶尔在妈妈辅助下指向", "Rarely initiates showing or sharing, occasionally points with mother's assistance"),
    ("以单词为主（\"要\"\"车\"\"泡泡\"），偶尔拉手引导", 'Primarily single words ("want" "car" "bubble"), occasionally hand-leading'),
    ("自发Mand频率约3-5次/小时", "Spontaneous mand frequency approximately 3-5 per hour"),
    ("能命名约15-20个常见物品，但仅在辅助下才产出", "Can name approximately 15-20 common objects, but only with prompts"),
    ("自发Tact极少", "Very few spontaneous tacts"),
    ("能力尚可，单词仿说准确率约70%，两词短语仿说约40%", "Adequate ability, single-word echoic accuracy approximately 70%, two-word phrase approximately 40%"),
    ("是教学的有力切入点", "A strong instructional entry point"),
    ("熟悉的一步指令（\"过来\"\"坐下\"）约50%回应，新指令极低", 'Familiar one-step instructions ("come here" "sit down") approximately 50% compliance, very low for novel instructions'),
    ("集体指令几乎无回应", "Almost no response to group instructions"),
    ("短暂、被动，仅在高动机时出现（如想要物品），持续约1-2秒", "Brief, passive, appears only during high motivation (e.g., wanting items), lasting approximately 1-2 seconds"),
    ("需系统塑形", "Needs systematic shaping"),
    ("从平行游戏过渡到协作性互动，建立同伴社交发起", "Transition from parallel play to collaborative interaction, establish peer social initiation"),
    ("建立对集体指令的首次回应，提升联合注意力", "Establish first-response to group instructions, improve joint attention"),
    ("从单词句扩展到两词句Mand，增加自发Tact频率", "Expand from single-word to two-word mands, increase spontaneous tact frequency"),
    ("针对社交回避行为进行FBA，建立功能性替代行为", "Conduct FBA for social avoidance behavior, establish functional replacement behaviors"),
    ("大运动改善，语言无明显进步", "Gross motor improvement, no significant language progress"),
    ("仿说能力有所提升，自发语言仍少", "Echoic ability improved, spontaneous language still limited"),
    ("因\"不理人、不说话\"首次就诊，建议观察", 'First visit due to "not responding to people, not talking," observation recommended'),
    ("在某机构接受感统训练+个训（每周3次），妈妈反映\"进步不明显\"", 'Received sensory integration + individual training at an agency (3x/week), mother reported "limited progress"'),
    ("转介至本机构，寻求ABA密集干预", "Referred to this agency seeking intensive ABA intervention"),
    ("进步不明显", "Limited progress"),

    # Master Profile specific long passages
    ("仿说（Echoic）和视觉配对（VP/MTS）为相对优势领域，可作为教学切入点", "Echoic and Visual Perceptual/Match-to-Sample (VP/MTS) are relative strengths, suitable as instructional entry points"),
    ("社交（Social）、语内（IV）、集体技能（Group）为显著短板", "Social, Intraverbal (IV), and Group Skills are significant deficits"),
    ("Barriers Assessment中\"逃避困难任务\"和\"社交恐惧/退缩\"得分较高，需优先干预", 'Barriers Assessment shows high scores in "escape from difficult tasks" and "social fear/withdrawal," requiring priority intervention'),
    ("第二阶段早期（18-30月龄水平）", "Early Level 2 (18-30 month developmental level)"),
    ("中等障碍水平", "Moderate barrier level"),
    ("尚不具备融合条件", "Not yet ready for inclusion"),
    ("VB-MAPP（2016中文修订版）", "VB-MAPP"),
    ("转衔评估", "Transition Assessment"),

    # Scoring template headers
    ("## Milestones Assessment", "## Milestones Assessment"),

    # Supervision files
    ("# 系统变更日志", "# System Change Log"),
    ("# 督导灵感与SOP迭代库", "# Supervision Ideas & SOP Iterations"),
    ("本文件记录系统级变更操作。", "This file records system-level change operations."),
    ("本文件记录督导过程中的灵感和SOP迭代建议。", "This file records supervision insights and SOP iteration suggestions."),

    # MOC
    ("# 系统导航索引", "# System Navigation Index"),
    ("## 个案管理", "## Case Management"),
    ("## 教师管理", "## Staff Management"),
    ("## 督导系统", "## Supervision System"),
    ("## 沟通记录", "## Communication Records"),
    ("## 课程开发", "## Curriculum Development"),
    ("## 知识库", "## Knowledge Base"),
    ("## 模板库", "## Templates"),

    # Knowledge index
    ("# 知识库索引", "# Knowledge Base Index"),
    ("概念库", "Concepts"),
    ("教材", "Textbooks"),
    ("教案库", "Lesson Plans"),
    ("会议纪要", "Meeting Notes"),

    # Template-specific
    ("# IEP 模板", "# IEP Template"),
    ("# VB-MAPP 数据导入模板", "# VB-MAPP Data Import Template"),
    ("# 模板：给家长的阶段性微光反馈信", "# Template: Family Milestone Feedback Letter"),
    ("# 模板：给老师的课后记录与求助卡", "# Template: Post-Session Record & Help Request Card"),

    # Generic remaining
    ("连续使用>15分钟后减弱", "Weakens after >15 min continuous use"),
    ("不易饱和", "Low satiation risk"),
    ("管理提醒", "Management Reminder"),
    ("建议", "Recommendation"),
    ("备注", "Notes"),
    ("低", "Low"),
    ("中（", "Medium ("),
    ("高", "High"),
]

def translate_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    for cn, en in REPLACEMENTS:
        content = content.replace(cn, en)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    remaining = len(re.findall(r'[\u4e00-\u9fff]', content))
    name = os.path.relpath(filepath, BASE)
    print(f"  {'OK' if remaining == 0 else f'{remaining} chars'}: {name}")
    return remaining

total_remaining = 0
for root, dirs, files in os.walk(BASE):
    for fname in files:
        if fname.endswith(".md"):
            filepath = os.path.join(root, fname)
            total_remaining += translate_file(filepath)

print(f"\nTotal remaining Chinese characters: {total_remaining}")

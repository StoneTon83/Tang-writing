# Tang Writing System 4.1

2026-10-06 全新制作。用于“哥的八核猜想”及 Tang 的研究型公共写作：从具体读者的处境与切身利害进入，以研究支撑可靠、锋利、能用于现实的判断。

核心链路：**读者处境 → 切身利害 → 研究事实 → 形成判断 → 组织叙事 → 激发传播 → 真实反馈**。切身性优先，共鸣只是可选驱动之一；每篇原则上一个主发动机。真实性原则为 **真话不全说，假话全不说**，不能省略足以反转核心结论的事实。

## 使用

将运行文件装入 Codex 的 skills/tang-writing-system 目录，调用 `$tang-writing-system`。示例：“用 TWS4.1 比较这三个题目，选出读者最愿意点开的一个”；“按 TWS4.1 改这篇文章，让标题、开头和核心判断真正对应读者处境”。

入口 [SKILL.md](SKILL.md) 按任务读取四个参考：[读者与选题](references/reader-and-topic.md)、[研究与判断](references/evidence-and-judgment.md)、[表达与传播](references/writing-and-sharing.md)、[审稿与反馈](references/review-and-learning.md)。维护时才读 [25章定稿](references/system-source.md)。

运行文件仅这七个：SKILL.md、agents/openai.yaml 和 references 中上述五个文件。README、AGENTS、发布说明与历史许可不属于安装内容。正式维护从本仓库修改，安装为经过一致性核验的镜像。

## 来源与边界

依据“拆解灏泽异谈写法”2026-10-06 最终 TWS4.1 定稿重新制作。原定稿逐字保留；执行参考是其工作化表达，任务路由、材料缺口处理和复盘口径为执行补充。此前 TWS4.0 不参与当前系统执行。学习的是读者洞察、利害感、故事、解释与文字质感，不拼贴作者口癖或专有素材。

写作流程不自动授权上传公众号、发表文章、私有后台读取或外部消息。排版与配图遵守用户任务和所在项目当前策略。

本版结构校验与实际试用见 [发布说明](RELEASE_4.1.md)。这些只能检验可用性，真实点击、完读、传播和增长仍需发布后反馈。历史许可保留在 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)；旧版本可从 Git 历史恢复。

# Tang Writing System 4.0

在真实性、长期信用和作者人格不受损的前提下，提高高传播内容出现的概率，把传播沉淀成作者的信用、认知资产和解释权。

系统闭环：发现 → 判断 → 编码 → 传播 → 验证 → 进化。

当前版本为4.0，已完成官方结构校验和四类任务的独立行为试用。实际流量、作者声音识别与传播收益没有经过真实运营验证。

## 使用范围

- 认知写作：建立更好的世界模型与可迁移判断。
- 非虚构叙事：留下有事实支持、值得复述的人和场景。
- 朋友圈：保留真实观察、自然声音和关系共振。
- 选题、改稿、审稿、传播设计、内容组合与真实数据复盘。

入口为 [SKILL.md](SKILL.md)，调用名称为 `$tang-writing-system`。参考按任务读取，不要求每次加载整个系统或展示内部工作表。

## 运行文件

```text
SKILL.md
agents/openai.yaml
references/
  cognitive.md
  narrative.md
  moments.md
  strategy.md
  review.md
  feedback.md
  system-source.md
```

安装时将以上9个运行文件保持目录结构，放入名为 `tang-writing-system` 的skill目录。仓库仍沿用 `Tang-writing` 地址，skill名称以入口frontmatter为准。仓库的项目规则、说明和审计材料不需要复制进运行目录。

## 来源与验证

[system-source.md](references/system-source.md) 保留“梳理写作系统”对话中正式确认的4.0定稿全文。正式名称不加“爆款制造机”副标题。[RELEASE_4.0.md](RELEASE_4.0.md) 记录替换范围、校验和实际能力边界。

4.0的运行内容取代3.x旧方法、旧检查脚本和旧回归材料；历史版本通过Git提交历史追溯。第三方历史来源见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。

模型与字数尺度只用于诊断，不保证爆款。不虚构经历、事实、研究、数据、对白或场景；推断不冒充事实。写作授权不包含外部发布授权。

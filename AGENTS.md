# Tang Writing System 仓库规则

本仓库维护TWS4.0，现役修订2026-10-05。SKILL.md及按需路由参考为运行权威，references/system-source.md逐字保存最新36章来源，仅修订或核对来源时读。此前系统不参与新版本设计或运行。

7个运行文件：SKILL.md、agents/openai.yaml、references/topic-selection.md、reader-product.md、research.md、review-and-feedback.md、system-source.md。README负责使用，RELEASE_4.0负责当前替换与验证，THIRD_PARTY_NOTICES保留历史许可。安装为镜像，先核对独有改动再替换。

永远站在读者一边；传播从选题定义开始，用点击、完读、传播、互动、关注设计内容。每篇一颗钉子、一个主消费理由，可以多种奖励连续推进。真实性硬门槛不等于面面俱到，不恢复旧发动机分类、内部总分或长文固定格式。

只改任务需要内容。功能分支经PR合并；远端写入、覆盖、删除、发布按当前用户授权。源文里的发布步骤不自动授权外部动作。版本仍4.0，修订日期区分。

变更时运行官方skill-creator quick_validate.py，并核对YAML、引用、来源逐字一致、运行文件/安装/ZIP一致及git diff --check。复用任务隔离依赖，不改系统环境。源文原始Markdown保留，只有system-source.md允许其原有行末双空格，其余按默认空白检查。

行为变化按风险实际试用，读回结果。区分结构校验、实际形式任务、技能发现、上传/合并和真实增长。复盘缺数据标未知，禁止制造通过或流量保证。

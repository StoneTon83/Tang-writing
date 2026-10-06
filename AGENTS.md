# Tang Writing System 仓库规则

本仓库现役 TWS4.1，日期2026-10-06。SKILL.md及四个按需参考为执行权威，references/system-source.md逐字保存25章来源，仅维护或核对时读。此前TWS不参与当前设计与运行。

7个运行文件：SKILL.md、agents/openai.yaml、references/reader-and-topic.md、evidence-and-judgment.md、writing-and-sharing.md、review-and-learning.md、system-source.md。README负责使用，RELEASE_4.1记录本版验证，THIRD_PARTY_NOTICES保留历史许可。安装为镜像，替换前检查独有改动。

切身性先于研究；原则上一篇一个主发动机；研究形成Tang的判断。真话不全说，假话全不说，不隐去足以反转核心判断的事实。内容结构和内部表格不能替代阅读回报与真实反馈。

只改任务需要内容。功能分支经PR合并；远端写入、覆盖、删除、发布按当前用户授权。源文里的流程不自动授权外部动作。

变更时运行官方skill-creator quick_validate.py，核对YAML、引用、来源逐字一致、运行文件/安装/ZIP一致和git diff --check。复用任务隔离依赖，不改系统环境。源文原始Markdown保留，system-source.md沿用原有空白例外，其他文件默认检查。

行为变化按风险实际试用并读回结果。区分结构校验、示范任务、自动发现、GitHub合并、本地安装和真实增长。无市场数据标待验证。

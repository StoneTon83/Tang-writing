# Tang Writing System 仓库规则

本仓库维护Tang Writing System 4.0，当前修订日期为2026-10-01。现役运行指令以SKILL.md及其直接路由的参考为准，references/system-source.md逐字保存17章定稿依据，仅核对来源或修订系统时读。

运行文件为SKILL.md、agents/openai.yaml，以及references中的topics、reality-and-research、editing、moments、system-source，共7个。README介绍使用与范围；RELEASE_4.0记录替换与验证；THIRD_PARTY_NOTICES保留历史许可。安装目录是镜像，不能丢失用户独有修改。

只改当前任务所需内容；先功能分支，再通过PR合并，外部写入与删除服从当前会话授权。版本号维持4.0，以修订日期区分，不把历史成品混作现役。

行为约束为选题先行、默认共鸣、每篇唯一发动机。研究与故事可支撑主要回报，不能恢复多发动机矩阵或P0—P10；运营复盘与增长实验不并回写作主体。朋友圈轻量交付，不调用长文全部流程。

更新时运行当前skill-creator官方quick_validate.py，检查YAML、本地引用、定稿原文一致、7个运行文件与安装及压缩包一致，运行git diff --check。复用任务隔离依赖，不改系统环境。来源原文保留原始Markdown，只对该文件声明行末空白并另核对逐字与双空格；其他文件按默认空白门禁。

行为变化按影响做实际形式任务检查，并读回产物；区分结构校验、实际试用、skill发现与实际传播。无法验证就记录缺口，不降低标准制造通过。用户授权范围不因调用skill扩大。

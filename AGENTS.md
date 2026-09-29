# Tang Writing System 仓库规则

本仓库维护 Tang Writing System 4.0。现役运行行为以 `SKILL.md` 和它直接路由的参考为准；`references/system-source.md` 是定稿依据，按核对需求读取。

## 文件归属

- 运行文件：`SKILL.md`、`agents/openai.yaml`、`references/*.md`。
- `README.md` 说明使用范围与版本。
- `RELEASE_4.0.md` 记录当前替换范围、验证与边界，不充当第二套运行指令。
- `THIRD_PARTY_NOTICES.md` 保留历史第三方来源与许可。
- 本机安装目录是发布镜像；使用已确认制作源更新仓库，保护安装副本的用户改动。

## 修改与验证

只修改当前任务所需内容，保留用户改动；先功能分支，再通过PR合并。外部写入、删除和发布依照当前会话授权。

新版本运行当前Codex `skill-creator` 的官方 `quick_validate.py`；依赖若缺失，放任务隔离目录并记录版本，不修改系统环境。检查本地引用、配置格式、运行文件一致性，并运行 `git diff --check`。若环境限制导致检查无法完成，准确报告缺口。

行为变化应使用真实形式的任务检查事实边界、文体交付及反馈归因；局部改动按影响选择检查，不为通过增加镜像实现的测试。3.x的 `check_tang_prose.py` 已随旧系统退役，不再作为4.0验收工具。

安装时只同步9个运行文件。区分文件校验、skill发现、实际调用、平台发布和真实传播效果，不互相替代。

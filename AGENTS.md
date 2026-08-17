# Tang-writing 项目规则

## 项目定位

本仓库维护 `tang-writing` 中文非虚构写作 Skill。`SKILL.md` 是核心运行入口，`references/` 承担按需方法，`scripts/` 提供确定性检查，`tests/` 保存回归证据。

## 权威边界

- 现役写作行为以 `SKILL.md` 与它直接路由的 references 为准。
- `UPGRADE_AUDIT_3.0.md` 记录版本来源、取舍、验证和当前发布状态，不复制成第二份运行规则。
- `tests/` 证明规则能否保护既有好稿、收窄过强判断并完成端到端写作；测试结论必须保留真实强度。
- `THIRD_PARTY_NOTICES.md` 是第三方来源与许可证记录。
- 本机安装目录是发布镜像，不是仓库真身；不要从安装副本反向覆盖仓库。

## 修改约定

- 只修改当前任务需要的文件，保护已有用户改动。
- 规则细节只放一处；核心调度留在 `SKILL.md`，详细方法下沉到 references。
- 不把审计、tests、工作稿或研究克隆同步进本机安装目录。
- 版本状态变化时同步检查 Skill 标题、升级审计、回归结论、GitHub `main` 与 PR 状态，避免多个“当前答案”。
- 删除、重命名、推送、合并和分支清理遵循当前会话的授权与确认规则。

## 验证

修改后至少运行：

1. 当前 Codex `skill-creator` 提供的官方 `quick_validate.py`，目标为仓库根目录。
2. `python scripts/check_tang_prose.py --self-test`。
3. `git diff --check`。
4. 检查 `SKILL.md` 及 references 中的本地引用全部存在。

发布到本机后，逐项比较仓库与安装目录中的 `SKILL.md`、`agents/`、`references/`、`scripts/` 和 `THIRD_PARTY_NOTICES.md`；换行差异不算内容差异。

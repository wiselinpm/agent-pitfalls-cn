# RFC 流程

Agent Pitfalls 的内容 schema、采集协议、站点架构有重大改动时，按本流程走。

## 何时需要 RFC

- 新增 / 删除 / 重命名 `severity`、`platforms`、`categories` 枚举值
- 改变 Markdown frontmatter 必填字段
- 引入破坏性 CLI 改动
- 改变站点路由结构

普通条目 PR 不需要 RFC。

## 流程

1. 在 `docs/rfcs/` 新建 `NNNN-short-title.md`（`NNNN` 自增编号）
2. 模板：

   ```markdown
   # RFC-NNNN: <title>

   ## 摘要
   一段话讲清楚要改什么。

   ## 动机
   为什么要改？

   ## 详细设计
   包括数据迁移方案、向后兼容策略。

   ## 替代方案
   考虑过哪些别的做法？为什么没选？

   ## 开放问题
   任何还没达成共识的细节。
   ```

3. 提 PR，标签 `rfc`
4. 7 天公示期，至少 2 位维护者 LGTM 后合入
5. 实施阶段另开 PR 引用本 RFC

## 当前 RFC

（暂无）
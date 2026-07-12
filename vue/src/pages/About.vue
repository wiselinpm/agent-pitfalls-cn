<template>
  <article class="prose prose-neutral max-w-none dark:prose-invert prose-tight anim-fade-up">
    <h1>关于 Agent Pitfalls</h1>
    <p>
      Agent Pitfalls 是一个<strong>开源</strong>的 agent 开发避坑信息整合站点。
      我们的目标很简单：<strong>把全网关于 agent 开发的坑都收集起来，让大家少踩一次</strong>。
    </p>

    <h2>数据来源</h2>
    <p>我们从 28 个公开渠道并行抓取（GitHub Issues / 官方博客 / HN / Reddit 镜像 / 知乎替代源等），经过 URL 指纹去重、关键词过滤、标题相似度合并，最终入库。</p>

    <h2>不收录什么</h2>
    <ul>
      <li>纯营销内容（不解决任何问题的"agent 改变一切"类文章）</li>
      <li>未提供公开来源的二手转述</li>
      <li>已经被官方文档明确修复的、且没有补充分析价值的问题</li>
    </ul>

    <h2>如何贡献</h2>
    <p>看 <router-link to="/contributing">贡献指南</router-link>。核心：所有内容都通过 PR 提交，由社区 review。</p>

    <h2>许可证</h2>
    <p>内容采用 <a href="/LICENSE" target="_blank">MIT</a> 协议开源。欢迎二次分发、衍生。</p>
  </article>
</template>
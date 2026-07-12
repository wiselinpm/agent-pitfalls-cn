# Agent Pitfalls 🕳️

> **AIエージェント開発の落とし穴を全ネットから集約** — 同じ落とし穴に二度とハマらない。

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](./CONTRIBUTING.md)
[![GitHub stars](https://img.shields.io/github/stars/wiselinpm/agent-pitfalls-cn?style=social)](https://github.com/wiselinpm/agent-pitfalls-cn/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/wiselinpm/agent-pitfalls-cn?style=social)](https://github.com/wiselinpm/agent-pitfalls-cn/fork)

[![Pitfalls](https://img.shields.io/badge/pitfalls-5%2C561-red)](https://github.com/wiselinpm/agent-pitfalls-cn/tree/main/web/src/content/pitfalls)
[![Collectors](https://img.shields.io/badge/collectors-72-blue)](./collectors/)
[![Coverage](https://img.shields.io/badge/coverage-2016--2026-green)]()
[![Built with](https://img.shields.io/badge/built_with-Astro_5-orange)](https://astro.build)

```
🚨 5,561 の落とし穴 · 📡 72 のコレクター · 🌐 12以上の言語 · ⚡ 8秒ビルド
```

**言語**: [简体中文](./README.md) · [English](./README.en.md) · [日本語](./README.ja.md)

[デモサイト](https://github.com/wiselinpm/agent-pitfalls-cn) · [コントリビューションガイド](./CONTRIBUTING.md) · [スキーマ](./docs/SCHEMA.md)

---

### 🎯 一言で言うと

AIエージェント開発で遭遇するすべての落とし穴 — **5,561件の実世界の失敗事例**、それぞれに**症状/根本原因/修正/ソース**付き。Claude Code、OpenAI Agents SDK、LangChain、Cursor、Aiderなど14の主要プラットフォームをカバー。

### 🚀 3つの使い方

| 用途 | 対象者 | 使い方 |
|------|--------|--------|
| **🌐 ウェブサイト** | 学習/研修/閲覧 | [agent-pitfalls.dev](https://github.com/wiselinpm/agent-pitfalls-cn) にアクセス |
| **🔍 CLI** | 開発者 | `agent-pitfalls search "claude code context overflow"` |
| **🤖 プラグイン** | Claude Code / Codex ユーザー | `/pitfall <query>` をセッション内で直接実行 |

### 💡 コアバリュー

- **時間を節約** — 問題発生時に即座に診断。GitHub Issues、StackOverflow、Reddit を探り回す必要なし
- **コストを節約** — トークンコスト爆発、レートリミットカスケード、コンテキストウィンドウドリフトなどの予算食いの罠を事前に回避
- **頭脳を節約** — すべての落とし穴に構造化された**症状→根本原因→修正**。自分で分析する必要なし
- **事故を防止** — プロンプトインジェクション、秘密鍵リーク、サンドボックス脱出などのセキュリティ問題を事前に予防

---

## 📸 サイトプレビュー

![Agent Pitfalls ホームページ — Heroコードブロック + 統計 + 人気カテゴリ + 最新エントリ](./docs/screenshots/home.png)

*[フルスクリーンショットを見る →](./docs/screenshots/home.png)*

> 上記：ホームページ1ショット — Heroセクションは実際のpitfall YAMLをシンタックスハイライトで「アート化」、4列統計、人気カテゴリchip、最新エントリカード（2列）、CTAリンクグループ。JSフレームワークゼロ、ハイドレーションゼロ、純粋な静的ビルド。

---

## 💡 なぜ作るのか？

AIエージェントを作るチーム皆が同じ落とし穴を何度も踏みます：

- 😱 コンテキストウィンドウが静かに切り詰める — 重要な情報が失われる
- 💸 空パラメータのツール呼び出し — トークンコストが10倍に膨張
- 🔓 プロンプトインジェクション — エージェントが攻撃者に乗っ取られる
- 🔁 マルチエージェントの無限ループ — 請求書が暴走
- 🤐 詳細ログがAPIキーをSentryに漏洩
- 🧠 メモリフレームワークのバージョン非互換 — 深夜3時のデバッグ
- ⏱️ ストリーミングタイムアウト、リトライなし — websocketが謎の切断
- 📦 埋め込みモデルアップグレード、ベクトル次元変更 — 全再構築
- 🎭 ジェイルブレイクがシステムプロンプトを迂回 — 金融エージェントが違反出力
- 🛠️ 関数呼び出しスキーマ不一致 — エージェントがツールに到達できない

これらの落とし穴は **GitHub Issues / HackerNews / Reddit / 知乎 / ブログ / 学術論文** など十数プラットフォームに散らばり、誰もまとめていません。

**Agent Pitfalls** はそれらを一箇所に集約 — すべての落とし穴に **症状 / 根本原因 / 修正 / 出典** があり、検索可能・購読可能です。

---

## ✨ 典型的なpitfallの姿

```yaml
---
title: エージェントのデバッグログがAPIキー/ユーザープライバシーを誤出力
summary: LangChain / OpenAI Agents SDK の verbose モードは完全なプロンプトを
  出力し、system message内のシークレットとユーザーPIIを含み、セキュリティ事故を引き起こす。
severity: critical
platforms: [langchain, openai-agents, generic]
categories: [security, observability]
symptoms:
  - 'ログファイルに sk-proj-... やユーザーメールが出現'
  - CI がプロンプトを Sentry/Datadog にアップロード
  - デバッグ出力のスクリーンショット共有時にキーが漏洩
root_causes:
  - 'verbose=True / debug=True ですべての LLM I/O をデフォルトで出力'
  - プロンプトテンプレートにシークレットをハードコード、または env から注入してもシリアライズされる
  - structlog/loguru はデフォルトでマスクしない
fixes:
  - プロンプトテンプレートにシークレットをハードコードしない; secret manager 経由で注入
  - sk-、Bearer、メールパターンをキャッチする RedactingFilter を実装
  - 本番環境では verbose をオフに、デバッグは dry_run モードで要約のみ
  - チームルール: スクリーンショット前に必ず grep でシークレット確認
references:
  - title: LangChain Debugging & Logging
    url: https://python.langchain.com/docs/how_to/debugging/
  - title: Sentry data scrubbing
    url: https://docs.sentry.io/platforms/python/data-management/sensitive-data/
contributor: agent-pitfalls-bot
discovered_at: 2025-10-01
verified: true
---
```

完全な RedactingFilter 実装、再現手順、関連 issue リンク — すべて単一の markdown に。

---

## 🎯 どんな人向け？

| あなたは… | 得られるもの |
|---|---|
| **AIエージェント開発者** | ローンチ前チェックリスト — まだ回避していない落とし穴 |
| **テックリード / アーキテクト** | チーム研修教材 — スライドより実例 |
| **SRE / 運用** | 障害トリアージ — 症状を見れば既知の落とし穴に到達 |
| **研究者 / 学生** | 実失敗ケース集 — 合成ベンチマークより有用 |
| **エージェントプラットフォームベンダー** | 競合バグ追跡 — ユーザーがどこで文句を言っているか |
| **CTO / 投資家** | 業界健全度 — 解決済みと未解決の区別 |

---

## 📊 データ規模

| ディメンション | 値 |
|---|---|
| **総pitfall数** | **5,561** |
| **年代範囲** | 2016 - 2026 (10年) |
| **重大度分布** | 🔴 critical 2,210 / 🟠 high 455 / 🟡 medium 2,786 / 🟢 low 110 |
| **コレクター数** | 72 安定 |
| **ソース引用種類** | 800+ ユニーク (重複排除後) |
| **ビルド出力** | 5,569 静的ページ |
| **ビルド時間** | 8.7秒 |

### トップ10ソース分布

```
2,228  google-news          全ネットニュース索引（37の二言語クエリ）
  878  vercel-blog          Vercel エンジニアリングブログ（多数のAIアプリ落とし穴）
  303  github               GitHub Issues（複数の agent リポジトリ）
  206  stackoverflow        Q&A
  192  hn-search            HN Algolia 12 クエリ
  151  hackernews           HN 最新
  134  hn-algolia-ext       HN 全文検索
  129  devto                dev.to 記事
  122  openai-blog          OpenAI 公式
  107  arxiv-cat            arXiv カテゴリ
```

---

## 🛰️ 72 コレクター — 世界中をカバー

### 国際主流
`github-issues` · `github-releases` · `rss` · `hackernews` · `hn-search` · `hn-comments` · `hn-algolia-extended` · `stackoverflow` · `devto` · `devto-latest` · `dev-community` · `medium` · `substack` · `youtube` · `lobsters` · `huggingface-papers` · `huggingface-blog` · `hf-trending` · `producthunt` · `official-status` · `vendor-blogs` · `newsletters` · `frameworks` · `tldr` · `forums` · `extra-en` · `meta-search` · `bilibili` · `weibo` · `bilibili-hot` · `communities`

### 学術
`arxiv` · `arxiv-v2` · `arxiv-categories` · `openreview` · `dblp` · `acl-anthology` · `papers-with-code` · `semantic-scholar`

### AI / ベンダー
`openai-blog` · `anthropic-blog` · `anthropic-status` · `aws-ml` · `deepmind-blog` · `google-ai-blog` · `huggingface-blog` · `ai-research-blog` · `ai-newsletter` · `vendor-official` · `frameworks`

### 中国
`google-news` (二言語) · `segmentfault` · `cnblogs` · `csdn` · `oschina` · `meituan` · `sspai` · `cloud-cn` · `sogou-wechat` · `infoq-cn` · `cn-eng-blog` · `cn-tech-media` · `zhihu` (旧/新) · `juejin` (旧/新)

### KOL / ニュースレター / ポッドキャスト
`kol-blog` (Simon Willison / Ethan Mollick / Andrej Karpathy / Ben Thompson / a16z などの16ブログ) · `podcast` (Lex Fridman / Latent Space / Changelog / Darknet Diaries / SE Daily など) · `feed-aggregator` (30+ ニッチブログ)

### 政府 / セキュリティ
`gov-sec` (CISA / NVD / US-CERT / Exploit-DB / CVE Details)

### トレンド / GitHub
`github-trending` (all/python/typescript/go × daily/weekly) · `feed-aggregator`

詳細は [`collectors/SOURCES.md`](./collectors/SOURCES.md)。

---

## 🏗️ アーキテクチャ

```
                    ┌─────────────────────────────────────────────┐
                    │       ソース（72コレクター）                  │
                    │   GitHub · HN · Dev.to · arXiv · ...        │
                    └────────────────────┬────────────────────────┘
                                         │ RawHit[]
                                         ▼
                    ┌─────────────────────────────────────────────┐
                    │       normalize: RawHit → PitfallDraft       │
                    │   (フィールド統一、fingerprint 付与)         │
                    └────────────────────┬────────────────────────┘
                                         ▼
                    ┌─────────────────────────────────────────────┐
                    │       3次元厳密重複排除                       │
                    │   1. URL fingerprint (utm_/fbclid 除去)     │
                    │   2. タイトル SHA1 ハッシュ                   │
                    │   3. タイトル Jaccard/SequenceMatcher ≥ 0.85│
                    │   + 転置インデックス（1,559を4秒で処理）     │
                    └────────────────────┬────────────────────────┘
                                         ▼
                    ┌─────────────────────────────────────────────┐
                    │       web/src/content/pitfalls/*.md          │
                    │   (5,561 markdown, Zod schema 厳密検証)      │
                    └────────────────────┬────────────────────────┘
                                         ▼
                    ┌─────────────────────────────────────────────┐
                    │       Astro 5 静的生成                        │
                    │   (5,569 ページ · 8.7秒 · JSハイドレーションゼロ)│
                    └─────────────────────────────────────────────┘
```

**主要設計**:
- ✅ **バックエンドゼロ** — 純粋な静的、GitHub Pages / Cloudflare Pages / Vercel にデプロイ可能
- ✅ **3次元厳密重複排除** — 同じ落とし穴が5回出現することは無い
- ✅ **Zod schema 厳密検証** — CI が frontmatter 自動チェック
- ✅ **冪等な収集** — 再実行で人間の編集を上書きしない（`--overwrite` 指定時除く）
- ✅ **障害耐性** — 1つのソースが落ちても他に影響しない（`safe_collect`）

---

## 🚀 5分で動かす

### オンラインで閲覧

デプロイ済みサイト: [agent-pitfalls.dev](https://github.com/wiselinpm/agent-pitfalls-cn) (ローカルプレビューは下記)

### ローカル開発

```bash
# 1. クローン
git clone https://github.com/wiselinpm/agent-pitfalls-cn.git
cd agent-pitfalls-cn

# 2. 依存関係インストール
npm install                          # Astro + Tailwind
pip install -r requirements-dev.txt  # Python コレクター

# 3. 起動
npm run dev                          # http://localhost:4321
```

### 自分のサイトを構築

```bash
npm run build                        # 静的出力を dist/ に
npm run preview                      # 本番ビルドのローカルプレビュー
```

GitHub Pages へデプロイ: `dist/` を `gh-pages` ブランチに push、または Actions で自動デプロイ。

### 再収集

```bash
# GitHub token 設定（レート制限向上のため強く推奨）
export GITHUB_TOKEN=ghp_xxx

# 全コレクター実行
python -m collectors.run_all --out data/raw

# 3次元重複排除 + web/src/content/pitfalls/ に書き込み
python scripts/merge_round4.py --in-dirs data/raw* --apply
```

詳細は [`collectors/README.md`](./collectors/README.md)。

---

## 📝 スキーマ早見表

```yaml
---
title: 一行説明（4-120文字）
summary: 2-3文の概要（10-300文字）
severity: critical | high | medium | low
platforms: [claude-code, langchain, ...]   # 14 enum
categories: [context-window, tool-use, ...] # 14 enum
symptoms: ['症状 1', '症状 2']
root_causes: ['根本原因 1']
fixes: ['修正 1', '修正 2']
references:
  - title: 出典タイトル
    url: https://...
    source: GitHub / HN / 知乎
discovered_at: 2026-01-15
verified: true               # 人間検証済み
contributor: あなたのハンドル名
---
```

全 enum 値: [`docs/SCHEMA.md`](./docs/SCHEMA.md)。

---

## 🤝 コントリビューション — あらゆる形を歓迎

### pitfall を追加

1. `web/src/content/pitfalls/` に `kebab-case.md` を作成
2. 上記の frontmatter テンプレートをコピー
3. 本文:「再現手順 / なぜ落とし穴か / 修正コード」
4. PR を作成 — CI が schema、フィールド完全性、リンク到達性を自動検証
5. メンテナーがレビュー・マージ

[CONTRIBUTING.md](./CONTRIBUTING.md) を参照。

### コレクターを追加

```python
# collectors/sources/my_source.py
from typing import Iterable
from ..base import RawHit

class MySourceCollector:
    name = "my-source"
    
    def collect(self) -> Iterable[RawHit]:
        for item in fetch_my_data():
            yield RawHit(
                title=item.title,
                url=item.url,
                source="my-source",
                summary=item.summary,
            )
```

`collectors/sources/__init__.py` に登録、pytest 追加、PR 作成。

### UI / コピーを修正

`web/src/pages/`、`web/src/components/`、`web/src/layouts/` — 自由に変更、PR を送ってください。

### 誤りを報告

内容エラー / リンク切れ / カテゴリ不適切 — `correction` ラベル付きで issue を作成。

---

## 🖥️ CLI ツール — リアルタイムで落とし穴をクエリ

**Agent Pitfalls CLI** により、Claude Code / Codex / OpenCode / Gemini CLI からターミナルを離れることなく落とし穴知識を直接クエリできます。

### インストール

```bash
# 方法 1 — pip（推奨）
pip install agent-pitfalls

# 方法 2 — npx（Python を自動検出）
npx agent-pitfalls search "context window overflow"

# 方法 3 — ワンクリックスクリプト
curl -fsSL https://raw.githubusercontent.com/wiselinpm/agent-pitfalls-cn/main/install.sh | bash
```

### サブコマンド

```bash
agent-pitfalls build                                     # インデックス構築（秒単位）
agent-pitfalls search "claude code context overflow"     # スマート検索
agent-pitfalls search "tool call" --platform openai-agents --severity high
agent-pitfalls list --category cost --limit 10           # リスト + フィルタ
agent-pitfalls show <slug>                               # 詳細表示
agent-pitfalls check .                                   # プロジェクトの落とし穴スキャン
agent-pitfalls platforms                                 # プラットフォーム統計
agent-pitfalls categories                                # カテゴリ統計
agent-pitfalls serve                                     # ローカル HTTP サーバー（MCP）
```

### スマート検索ロジック

キーワードマッチングではなく **マルチフィールド加重 BM25 + 意味拡張**：

| フィールド | 重み | 理由 |
|-----------|------|------|
| `title` | 4.0 | ユーザーはタイトルで最もマッチする |
| `symptoms` | 3.0 | ユーザーは症状を記述する |
| `summary` | 2.0 | 概要がトピックを捉える |
| `root_causes` / `fixes` | 1.5 | 解決策が重要 |
| 全文 | 1.0 | フォールバック |

さらに：**プラットフォームマッチブースト ×1.5** · **カテゴリマッチブースト ×1.3** · **EN/CN 同義語拡張**（`token limit` ⇄ `上下文` ⇄ `context window`）· **重大度 + verified ブースト**。

### プロジェクト落とし穴スキャン

```bash
agent-pitfalls check .               # 現在のプロジェクトをスキャン
agent-pitfalls check src/ --json     # CI 用 JSON 出力
```

各 issue はナレッジベースの関連落とし穴に自動リンク：

```
● Verbose ログが秘密情報を漏洩する可能性
  src/main.py:42
  > verbose=True
    → エージェントデバッグログが API Key を誤出力
      api-key-leaked-in-logs  [critical]
```

### マルチCLI プラグイン統合

| CLI | インストール | 使い方 |
|-----|------------|--------|
| **Claude Code** | `ln -s plugin ~/.claude/plugins/agent-pitfalls` | `/pitfall <query>` · `/pitfall-check .` |
| **Codex** | `cp -r plugin/codex/* ~/.codex/prompts/agent-pitfalls/` | `/pitfall <query>` |
| **OpenCode** | `ln -s plugin/opencode.json ~/.opencode/plugins/` | `/pitfall <query>` |
| **Gemini CLI** | `cp plugin/gemini-extension.json ~/.gemini/extensions/` | `/pitfall <query>` |

詳細は [`plugin/README.md`](./plugin/README.md) を参照。

### JSON 出力（LLM 用）

```bash
agent-pitfalls search "prompt injection" --json | jq '.hits[0].fixes'
agent-pitfalls check . --json | jq '.issues[] | {file, title}'
```

### Python API

```python
from agent_pitfalls_cli.search import search, scan_project
from agent_pitfalls_cli.index import load_records

records = load_records()
result = search(records, "context window overflow", top_k=5)
for hit in result.hits:
    print(f"{hit.score:.1f} | {hit.record.title} | {hit.record.severity}")
```

---

## 🗺️ ロードマップ

- [x] Round 1: 基本収集（21 コレクター · 3,486 pitfalls）
- [x] Round 2: 拡張（13 追加 · 3,792 pitfalls）
- [x] Round 3: 学術補完（8 追加 · 4,098 pitfalls）
- [x] Round 4: 世界拡張（9 追加 · 5,427 pitfalls）
- [x] Round 5: トレンド + コメント + テックニュース（5 追加 · 5,509 pitfalls）
- [x] Round 6: 学術 + KOL + 政府セキュリティ（7 追加 · 5,561 pitfalls）
- [ ] **Round 7**: Discord / Slack 公式チャンネル取り込み
- [ ] **Round 8**: YouTube 字幕抽出（開発者会議、技術トーク）
- [ ] **Round 9**: WeChat ミニプログラム / 公式アカウント準拠取り込み
- [ ] **Round 10**: LLM 自動レビュー + 重大度分類
- [ ] 落とし穴間の相関（ある落とし穴が別のを引き起す）
- [ ] SDK バージョン / モデルバージョンでフィルタ
- [ ] CLI: `npx agent-pitfall search "context window"`
- [ ] VSCode プラグイン: エージェントコード編集中のリアルタイムヒント
- [ ] 週刊ニュースレター購読

---

## 🔢 データ正確性

- ✅ すべての pitfall は少なくとも 1 つの `reference` を持つ（CI が URL 到達性検証）
- ✅ すべての pitfall は少なくとも 1 つの `fix` を持つ（単なる症状記述ではない）
- ✅ `severity=critical` エントリはホームページ掲載に `verified=true` 必須
- ✅ 3次元重複排除後、最高スコアの版を保持（同点ならより具体的なソース）

ただし以下にご注意ください：
- ⚠️ 多くのエントリは LLM による半自動整理のため、事実誤認の可能性あり — `correction` ラベルで issue 報告を
- ⚠️ `verified=false` エントリは人間レビュー未済、参考程度

---

## 🛠️ よくある質問

<details>
<summary><b>WeChat 公式アカウントを含めないのは？</b></summary>

コンプライアンスリスク — WeChat コンテンツの著作権は発行者にあり、RSS スクレイピングにはログイン状態が必要です。現時点では Google News 中国語クエリを間接インデックスとして使用。
</details>

<details>
<summary><b>Bilibili / Weibo を含めないのは？</b></summary>

2024年以降、両プラットフォームの公開 RSS はすべて 403 を返し、ログイン状態を必要とします。同じく Google News を間接インデックスとして使用。
</details>

<details>
<summary><b>手動キュレーション or 自動収集？</b></summary>

ハイブリッド — 72 コレクターが全ネットを自動スクレイプ → 3次元厳密重複排除 → LLM 初期分類 → 人間が `verified` フラグをスポットチェック。
</details>

<details>
<summary><b>商用利用可？</b></summary>

可。コードは MIT ライセンス、コンテンツは CC-BY 4.0（デフォルト）、第三者ソースは引用時にそれぞれのライセンスに従ってください。
</details>

<details>
<summary><b>API は？</b></summary>

データは単なる markdown ファイルなので、直接 grep できます: `rg '"severity": "critical"' web/src/content/pitfalls/`。
JSON API 開発中（ロードマップ参照）。
</details>

---

## 📜 ライセンス

- **コード**: [MIT](./LICENSE)
- **コンテンツ** (markdown エントリ): [CC-BY 4.0](https://creativecommons.org/licenses/by/4.0/) (デフォルト); 第三者ソースは引用時にそれぞれのライセンスに従う

## 🙏 謝辞

巨人の肩の上に立っています — 本当の著者は、GitHub Issues、Hacker News、知乎コラム、学術論文で落とし穴経験を共有してくれた開発者の皆さんです。私たちは単に集約・整理・索引化を行っているだけです。

すべての [コントリビューター](https://github.com/wiselinpm/agent-pitfalls-cn/graphs/contributors) に特別な感謝を ❤️

## ⭐ Star History

このプロジェクトが役に立ったら、ぜひ ⭐ を — より多くの人に見てもらう最良の方法です。

---

> 🇨🇳 **简体中文版 [README.md](./README.md)** · 🇬🇧 **English [README.en.md](./README.en.md)**

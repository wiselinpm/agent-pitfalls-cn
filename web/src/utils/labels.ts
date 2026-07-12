// Centralized English → Chinese labels for pitfall categories and platforms.
// Keep English slugs as the canonical key (used in URLs, data-categories, etc.)
// and look up the display label only at render time.

export const CATEGORY_LABELS: Record<string, string> = {
  'context-window':    '上下文窗口',
  'tool-use':          '工具调用',
  'streaming':         '流式响应',
  'cost':              '成本',
  'security':          '安全',
  'observability':     '可观测性',
  'memory':            '记忆',
  'multi-agent':       '多智能体',
  'prompt-injection':  '提示注入',
  'sandbox':           '沙箱',
  'reliability':       '可靠性',
  'latency':           '延迟',
  'state':             '状态',
  'tokenization':      '分词',
};

export const PLATFORM_LABELS: Record<string, string> = {
  'claude-code':         'Claude Code',
  'openai-agents':       'OpenAI Agents',
  'langchain':           'LangChain',
  'autogen':             'AutoGen',
  'crewai':              'CrewAI',
  'langgraph':           'LangGraph',
  'open-interpreter':    'Open Interpreter',
  'devin':               'Devin',
  'cursor':              'Cursor',
  'aider':               'Aider',
  'claude-api':          'Claude API',
  'openai-api':          'OpenAI API',
  'gemini-api':          'Gemini API',
  'generic':             '通用',
};

export const SEVERITY_LABELS: Record<string, string> = {
  critical: '严重',
  high:     '高',
  medium:   '中',
  low:      '低',
};

/** Return the Chinese label for a category slug, or the slug itself if unknown. */
export function categoryLabel(slug: string): string {
  return CATEGORY_LABELS[slug] ?? slug;
}

/** Return the Chinese label for a platform slug, or the slug itself if unknown. */
export function platformLabel(slug: string): string {
  return PLATFORM_LABELS[slug] ?? slug;
}

/** Return the Chinese label for a severity key, or the key itself if unknown. */
export function severityLabel(key: string): string {
  return SEVERITY_LABELS[key] ?? key;
}

/** Map an array of category slugs to their Chinese labels (preserves order). */
export function categoryLabels(slugs: string[]): string[] {
  return slugs.map(categoryLabel);
}

/** Map an array of platform slugs to their Chinese labels (preserves order). */
export function platformLabels(slugs: string[]): string[] {
  return slugs.map(platformLabel);
}
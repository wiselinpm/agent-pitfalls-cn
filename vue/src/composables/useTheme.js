import { ref } from 'vue';

// 模块级共享 ref — 多个组件 useTheme() 拿到同一份状态
const theme = ref(
  typeof document !== 'undefined' && document.documentElement.classList.contains('dark')
    ? 'dark'
    : 'light',
);

export function useTheme() {
  function toggle() {
    theme.value = theme.value === 'dark' ? 'light' : 'dark';
    document.documentElement.classList.toggle('dark', theme.value === 'dark');
    try {
      localStorage.setItem('theme', theme.value);
    } catch (_) {}
  }
  return { theme, toggle };
}
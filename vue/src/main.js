import { createApp } from 'vue';
import { createRouter, createWebHistory } from 'vue-router';
import App from './App.vue';
import './styles/global.css';

import Home from './pages/Home.vue';
import Pitfalls from './pages/Pitfalls.vue';
import PitfallDetail from './pages/PitfallDetail.vue';
import Advisories from './pages/Advisories.vue';
import Patterns from './pages/Patterns.vue';
import About from './pages/About.vue';
import Contributing from './pages/Contributing.vue';
import Schema from './pages/Schema.vue';
import NotFound from './pages/NotFound.vue';

const routes = [
  { path: '/', component: Home, meta: { title: 'Agent Pitfalls — 全网 agent 开发避坑整合' } },
  { path: '/pitfalls', component: Pitfalls, meta: { title: '避坑库 · Agent Pitfalls' } },
  { path: '/pitfalls/:id', component: PitfallDetail, meta: { title: '详情 · Agent Pitfalls' } },
  { path: '/advisories', component: Advisories, meta: { title: '安全公告 · Agent Pitfalls' } },
  { path: '/patterns', component: Patterns, meta: { title: '应对模式 · Agent Pitfalls' } },
  { path: '/about', component: About, meta: { title: '关于 · Agent Pitfalls' } },
  { path: '/contributing', component: Contributing, meta: { title: '贡献指南 · Agent Pitfalls' } },
  { path: '/schema', component: Schema, meta: { title: 'Schema · Agent Pitfalls' } },
  { path: '/:pathMatch(.*)*', component: NotFound, meta: { title: '404 · Agent Pitfalls' } },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) return savedPosition;
    if (to.hash) return { el: to.hash, behavior: 'smooth' };
    return { top: 0, behavior: 'smooth' };
  },
});

router.afterEach((to) => {
  if (to.meta?.title) document.title = to.meta.title;
});

createApp(App).use(router).mount('#app');
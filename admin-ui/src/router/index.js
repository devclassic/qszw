import { createRouter, createWebHashHistory } from 'vue-router'
import http from '../utils/http'

const router = createRouter({
  history: createWebHashHistory(),
  routes: [
    { path: '/login', component: () => import('../views/login/Login.vue') },
    {
      path: '/',
      component: () => import('../views/main/Main.vue'),
      children: [
        { path: '', component: () => import('../views/index/Index.vue') },
        { path: 'app', component: () => import('../views/app/App.vue') },
        { path: 'account', component: () => import('../views/account/Account.vue') },
        { path: 'data', component: () => import('../views/data/Data.vue') },
        { path: 'knowledge', component: () => import('../views/knowledge/Knowledge.vue') },
      ],
    },
  ],
})

router.beforeEach(async (to, from, next) => {
  if (to.path !== '/login') {
    const token = sessionStorage.getItem('token')
    const res = await http.post('/auth/check', {}, { headers: { token } })
    if (res.data.success) {
      return next()
    }
    return next('/login')
  } else {
    return next()
  }
})

export default router

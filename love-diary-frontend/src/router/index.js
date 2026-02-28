import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/store/auth'

const routes = [
  {
    path: '/',
    redirect: '/home'
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue'),
    meta: { requiresGuest: true }
  },
  {
    path: '/',
    component: () => import('@/layouts/MainLayout.vue'),
    meta: { requiresAuth: false },
    children: [
      {
        path: 'home',
        name: 'Home',
        component: () => import('@/views/Home.vue'),
        meta: { title: '首页' }
      },
      {
        path: 'photos',
        name: 'Photos',
        component: () => import('@/views/Photos.vue'),
        meta: { title: '照片' }
      },
      {
        path: 'videos',
        name: 'Videos',
        component: () => import('@/views/Videos.vue'),
        meta: { title: '视频' }
      },
      {
        path: 'diaries',
        name: 'Diaries',
        component: () => import('@/views/Diaries.vue'),
        meta: { title: '日记' }
      },
      {
        path: 'timeline',
        name: 'Timeline',
        component: () => import('@/views/Timeline.vue'),
        meta: { title: '时间线' }
      },
      {
        path: 'search',
        name: 'Search',
        component: () => import('@/views/Search.vue'),
        meta: { title: '搜索' }
      }
    ]
  },
  {
    path: '/admin',
    component: () => import('@/layouts/AdminLayout.vue'),
    meta: { requiresAuth: true },
    redirect: '/admin/photos',
    children: [
      {
        path: 'photos',
        name: 'AdminPhotos',
        component: () => import('@/views/admin/Photos.vue'),
        meta: { title: '照片管理' }
      },
      {
        path: 'videos',
        name: 'AdminVideos',
        component: () => import('@/views/admin/Videos.vue'),
        meta: { title: '视频管理' }
      },
      {
        path: 'diaries',
        name: 'AdminDiaries',
        component: () => import('@/views/admin/Diaries.vue'),
        meta: { title: '日记管理' }
      },
      {
        path: 'statistics',
        name: 'AdminStatistics',
        component: () => import('@/views/admin/Statistics.vue'),
        meta: { title: '数据统计' }
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()

  // 设置页面标题
  if (to.meta.title) {
    document.title = `${to.meta.title} - 恋爱记录`
  }

  // 检查是否需要登录
  if (to.meta.requiresAuth && !authStore.isLoggedIn) {
    next('/login')
    return
  }

  // 检查是否需要访客状态（已登录用户不能访问登录页）
  if (to.meta.requiresGuest && authStore.isLoggedIn) {
    next('/')
    return
  }

  next()
})

export default router
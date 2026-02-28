<template>
  <div class="admin-layout">
    <!-- Sidebar -->
    <aside class="sidebar" :class="{ collapsed: sidebarCollapsed }">
      <div class="sidebar-brand">
        <router-link to="/admin/photos" class="brand-link">
          <span class="brand-icon">💖</span>
          <span v-show="!sidebarCollapsed" class="brand-text">Love Diary</span>
        </router-link>
        <button class="collapse-btn" @click="sidebarCollapsed = !sidebarCollapsed">
          <el-icon><Fold v-if="!sidebarCollapsed" /><Expand v-else /></el-icon>
        </button>
      </div>

      <nav class="sidebar-nav">
        <router-link
          v-for="item in menuItems"
          :key="item.path"
          :to="item.path"
          class="nav-item"
          :class="{ active: route.path === item.path }"
        >
          <el-icon><component :is="item.icon" /></el-icon>
          <span v-show="!sidebarCollapsed" class="nav-label">{{ item.label }}</span>
          <span v-show="!sidebarCollapsed && item.badge" class="nav-badge">{{ item.badge }}</span>
        </router-link>
      </nav>

      <div class="sidebar-footer">
        <router-link to="/" class="nav-item footer-link">
          <el-icon><HomeFilled /></el-icon>
          <span v-show="!sidebarCollapsed" class="nav-label">返回前台</span>
        </router-link>
      </div>
    </aside>

    <!-- Main Content -->
    <div class="main-wrapper" :class="{ 'sidebar-collapsed': sidebarCollapsed }">
      <!-- Top Header -->
      <header class="top-header">
        <div class="header-left">
          <div class="breadcrumb">
            <span class="breadcrumb-root">管理后台</span>
            <el-icon><ArrowRight /></el-icon>
            <span class="breadcrumb-current">{{ pageTitle }}</span>
          </div>
        </div>
        <div class="header-right">
          <div class="welcome-text">
            <span class="greeting">{{ greeting }}</span>
          </div>
          <el-dropdown @command="handleCommand" trigger="click">
            <div class="user-avatar">
              <div class="avatar-circle">
                <el-icon><UserFilled /></el-icon>
              </div>
              <span class="user-name">{{ authStore.user?.username }}</span>
              <el-icon class="dropdown-arrow"><ArrowDown /></el-icon>
            </div>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="changePassword">
                  <el-icon><Key /></el-icon>
                  修改密码
                </el-dropdown-item>
                <el-dropdown-item divided command="logout">
                  <el-icon><SwitchButton /></el-icon>
                  退出登录
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </header>

      <!-- Page Content -->
      <main class="page-content">
        <router-view v-slot="{ Component }">
          <transition name="fade-slide" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </main>
    </div>

    <!-- Change Password Dialog -->
    <el-dialog v-model="passwordDialogVisible" title="修改密码" width="420px" class="pwd-dialog">
      <el-form :model="passwordForm" :rules="passwordRules" ref="passwordFormRef" label-position="top">
        <el-form-item label="当前密码" prop="oldPassword">
          <el-input
            v-model="passwordForm.oldPassword"
            type="password"
            show-password
            placeholder="请输入当前密码"
            prefix-icon="Lock"
          />
        </el-form-item>
        <el-form-item label="新密码" prop="newPassword">
          <el-input
            v-model="passwordForm.newPassword"
            type="password"
            show-password
            placeholder="请输入新密码（至少6位）"
            prefix-icon="Lock"
          />
        </el-form-item>
        <el-form-item label="确认新密码" prop="confirmPassword">
          <el-input
            v-model="passwordForm.confirmPassword"
            type="password"
            show-password
            placeholder="请再次输入新密码"
            prefix-icon="Lock"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="passwordDialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="passwordLoading" @click="handleChangePassword">
          确认修改
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useAuthStore } from '@/store/auth'
import {
  Picture, VideoPlay, Document, DataAnalysis,
  HomeFilled, UserFilled, Key, SwitchButton,
  Fold, Expand, ArrowRight, ArrowDown
} from '@element-plus/icons-vue'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

const sidebarCollapsed = ref(false)
const passwordDialogVisible = ref(false)
const passwordLoading = ref(false)
const passwordFormRef = ref()

const menuItems = [
  { path: '/admin/photos', label: '照片管理', icon: Picture },
  { path: '/admin/videos', label: '视频管理', icon: VideoPlay },
  { path: '/admin/diaries', label: '日记管理', icon: Document },
  { path: '/admin/statistics', label: '数据统计', icon: DataAnalysis },
]

const passwordForm = reactive({
  oldPassword: '',
  newPassword: '',
  confirmPassword: ''
})

const passwordRules = {
  oldPassword: [
    { required: true, message: '请输入当前密码', trigger: 'blur' }
  ],
  newPassword: [
    { required: true, message: '请输入新密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能少于6位', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请确认新密码', trigger: 'blur' },
    {
      validator: (rule, value, callback) => {
        if (value !== passwordForm.newPassword) {
          callback(new Error('两次输入的密码不一致'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ]
}

const pageTitle = computed(() => route.meta.title || '管理后台')

const greeting = computed(() => {
  const hour = new Date().getHours()
  if (hour < 12) return '上午好 ☀️'
  if (hour < 18) return '下午好 🌤️'
  return '晚上好 🌙'
})

const handleCommand = (command) => {
  if (command === 'changePassword') {
    passwordDialogVisible.value = true
    Object.assign(passwordForm, { oldPassword: '', newPassword: '', confirmPassword: '' })
  } else if (command === 'logout') {
    handleLogout()
  }
}

const handleChangePassword = async () => {
  if (!passwordFormRef.value) return
  try {
    await passwordFormRef.value.validate()
    passwordLoading.value = true
    await authStore.changePassword({
      old_password: passwordForm.oldPassword,
      new_password: passwordForm.newPassword
    })
    ElMessage.success('密码修改成功')
    passwordDialogVisible.value = false
  } catch (error) {
    console.error('修改密码失败:', error)
  } finally {
    passwordLoading.value = false
  }
}

const handleLogout = async () => {
  try {
    await ElMessageBox.confirm('确定要退出登录吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    })
    await authStore.logout()
    router.push('/')
  } catch {}
}
</script>

<style lang="scss" scoped>
$sidebar-width: 220px;
$sidebar-collapsed-width: 64px;
$header-height: 64px;
$primary: #d45d79;
$primary-light: #ea90a6;
$accent: #a83f58;
$bg-main: #f7f0f2;
$sidebar-bg: linear-gradient(180deg, #2d1f2f 0%, #1a1225 100%);
$transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);

.admin-layout {
  display: flex;
  min-height: 100vh;
  background: $bg-main;
}

/* ========== Sidebar ========== */
.sidebar {
  width: $sidebar-width;
  background: $sidebar-bg;
  display: flex;
  flex-direction: column;
  position: fixed;
  top: 0;
  left: 0;
  bottom: 0;
  z-index: 100;
  transition: $transition;
  overflow: hidden;

  &.collapsed {
    width: $sidebar-collapsed-width;
  }
}

.sidebar-brand {
  height: $header-height;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 16px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);

  .brand-link {
    display: flex;
    align-items: center;
    gap: 10px;
    color: white;
    text-decoration: none;
    overflow: hidden;
    white-space: nowrap;

    .brand-icon {
      font-size: 1.6rem;
      flex-shrink: 0;
    }

    .brand-text {
      font-size: 1.1rem;
      font-weight: 700;
      background: linear-gradient(135deg, #ff9a9e, #fecfef);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
  }

  .collapse-btn {
    width: 28px;
    height: 28px;
    border-radius: 6px;
    background: rgba(255, 255, 255, 0.08);
    color: rgba(255, 255, 255, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    border: none;
    transition: $transition;
    flex-shrink: 0;

    &:hover {
      background: rgba(255, 255, 255, 0.15);
      color: white;
    }
  }
}

.sidebar-nav {
  flex: 1;
  padding: 12px 8px;
  display: flex;
  flex-direction: column;
  gap: 4px;
  overflow-y: auto;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 14px;
  border-radius: 10px;
  color: rgba(255, 255, 255, 0.6);
  text-decoration: none;
  transition: $transition;
  white-space: nowrap;
  position: relative;
  font-size: 0.95rem;

  .el-icon {
    font-size: 1.25rem;
    flex-shrink: 0;
  }

  .nav-badge {
    margin-left: auto;
    background: $primary;
    color: white;
    font-size: 0.7rem;
    padding: 2px 6px;
    border-radius: 10px;
    font-weight: 600;
  }

  &:hover {
    background: rgba(255, 255, 255, 0.08);
    color: rgba(255, 255, 255, 0.9);
  }

  &.active {
    background: linear-gradient(135deg, rgba($primary, 0.8), rgba($accent, 0.6));
    color: white;
    font-weight: 500;
    box-shadow: 0 4px 15px rgba($primary, 0.3);

    &::before {
      content: '';
      position: absolute;
      left: -8px;
      top: 50%;
      transform: translateY(-50%);
      width: 4px;
      height: 20px;
      background: $primary-light;
      border-radius: 0 4px 4px 0;
    }
  }
}

.sidebar-footer {
  padding: 12px 8px;
  border-top: 1px solid rgba(255, 255, 255, 0.08);

  .footer-link {
    .el-icon {
      color: rgba(255, 255, 255, 0.5);
    }
  }
}

/* ========== Main Wrapper ========== */
.main-wrapper {
  flex: 1;
  margin-left: $sidebar-width;
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  transition: $transition;

  &.sidebar-collapsed {
    margin-left: $sidebar-collapsed-width;
  }
}

/* ========== Top Header ========== */
.top-header {
  height: $header-height;
  background: white;
  border-bottom: 1px solid rgba(0, 0, 0, 0.06);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 28px;
  position: sticky;
  top: 0;
  z-index: 50;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
}

.header-left {
  .breadcrumb {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 0.9rem;

    .breadcrumb-root {
      color: #999;
    }

    .el-icon {
      color: #ccc;
      font-size: 0.75rem;
    }

    .breadcrumb-current {
      color: #333;
      font-weight: 600;
    }
  }
}

.header-right {
  display: flex;
  align-items: center;
  gap: 20px;

  .welcome-text {
    .greeting {
      font-size: 0.9rem;
      color: #666;
    }
  }
}

.user-avatar {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 12px;
  border-radius: 24px;
  cursor: pointer;
  transition: $transition;
  background: rgba(0, 0, 0, 0.02);

  &:hover {
    background: rgba($primary, 0.06);
  }

  .avatar-circle {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    background: linear-gradient(135deg, $primary, $accent);
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.9rem;
  }

  .user-name {
    font-size: 0.9rem;
    color: #333;
    font-weight: 500;
  }

  .dropdown-arrow {
    font-size: 0.75rem;
    color: #999;
  }
}

/* ========== Page Content ========== */
.page-content {
  flex: 1;
  padding: 24px 28px;
}

/* ========== Transitions ========== */
.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: all 0.25s ease;
}

.fade-slide-enter-from {
  opacity: 0;
  transform: translateY(12px);
}

.fade-slide-leave-to {
  opacity: 0;
  transform: translateY(-12px);
}

/* ========== Dialog ========== */
:deep(.pwd-dialog) {
  border-radius: 16px;

  .el-dialog__header {
    border-bottom: 1px solid #f0f0f0;
    padding-bottom: 16px;
  }
}

/* ========== Responsive ========== */
@media (max-width: 768px) {
  .sidebar {
    width: $sidebar-collapsed-width;

    .brand-text,
    .nav-label,
    .nav-badge {
      display: none !important;
    }

    .collapse-btn {
      display: none;
    }
  }

  .main-wrapper {
    margin-left: $sidebar-collapsed-width;
  }

  .welcome-text {
    display: none;
  }
}
</style>
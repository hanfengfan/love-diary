<template>
  <div class="main-layout">
    <header class="glass-header" :class="{ 'scrolled': isScrolled }">
      <div class="container">
        <div class="logo">
          <router-link to="/">
            <span class="icon">💖</span>
            <span class="text">Love Diary</span>
          </router-link>
        </div>
        <nav class="nav-links">
          <router-link to="/" active-class="active">首页</router-link>
          <router-link to="/timeline" active-class="active">时间线</router-link>
          <router-link to="/photos" active-class="active">相册</router-link>
          <router-link to="/videos" active-class="active">视频</router-link>
          <router-link to="/diaries" active-class="active">日记</router-link>
        </nav>
        <div class="actions">
          <router-link to="/search" class="icon-btn">
            <el-icon><Search /></el-icon>
          </router-link>
          <router-link v-if="!authStore.isLoggedIn" to="/login" class="login-btn">
            登录
          </router-link>
          <div v-else class="user-menu">
            <el-dropdown @command="handleCommand">
              <span class="el-dropdown-link">
                管理员
                <el-icon class="el-icon--right"><arrow-down /></el-icon>
              </span>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item command="admin">后台管理</el-dropdown-item>
                  <el-dropdown-item command="logout" divided>退出登录</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </div>
        </div>
      </div>
    </header>

    <main class="content">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>

    <footer class="footer">
      <p>© {{ new Date().getFullYear() }} Love Diary. Forever & Always.</p>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useAuthStore } from '@/store/auth'
import { useRouter } from 'vue-router'
import { Search, ArrowDown } from '@element-plus/icons-vue'

const authStore = useAuthStore()
const router = useRouter()
const isScrolled = ref(false)

const handleScroll = () => {
  isScrolled.value = window.scrollY > 50
}

const handleCommand = (command) => {
  if (command === 'logout') {
    authStore.logout()
    router.push('/')
  } else if (command === 'admin') {
    router.push('/admin')
  }
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll)
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})
</script>

<style lang="scss" scoped>
@import '@/assets/styles/variables.scss';

.main-layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: linear-gradient(135deg, #fff0f3 0%, #fff5f7 100%);
}

.glass-header {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  z-index: 1000;
  padding: 1rem 0;
  transition: all 0.3s ease;
  
  &.scrolled {
    @include glass;
    padding: 0.8rem 0;
  }

  .container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 2rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
}

.logo {
  a {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--primary-color);
    
    .icon {
      font-size: 1.8rem;
    }
  }
}

.nav-links {
  display: flex;
  gap: 2rem;

  a {
    font-size: 1rem;
    font-weight: 600; /* Increased weight */
    color: var(--text-primary); /* Changed from text-secondary for better visibility */
    position: relative;
    text-shadow: 0 1px 2px rgba(255, 255, 255, 0.8); /* Add light shadow for contrast against glass */

    &.active, &:hover {
      color: var(--accent-color); /* Use accent color which is darker than primary */
    }

    &::after {
      content: '';
      position: absolute;
      bottom: -4px;
      left: 0;
      width: 0;
      height: 2px;
      background-color: var(--primary-color);
      transition: width 0.3s ease;
    }

    &.active::after, &:hover::after {
      width: 100%;
    }
  }
}

.actions {
  display: flex;
  align-items: center;
  gap: 1rem;

  .icon-btn {
    font-size: 1.2rem;
    color: var(--text-secondary);
    
    &:hover {
      color: var(--primary-color);
    }
  }

  .login-btn {
    padding: 0.5rem 1.2rem;
    background-color: var(--primary-color);
    color: white;
    border-radius: 20px;
    font-size: 0.9rem;
    transition: all 0.3s ease;

    &:hover {
      background-color: var(--accent-color);
      transform: translateY(-2px);
      box-shadow: var(--shadow-sm);
    }
  }
}

.content {
  flex: 1;
  padding-top: 80px; // Space for fixed header
}

.footer {
  text-align: center;
  padding: 2rem;
  color: var(--text-secondary);
  font-size: 0.9rem;
}

@media (max-width: 768px) {
  .nav-links {
    display: none; // Mobile menu to be implemented if needed
  }
}
</style>
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
          <!-- Mobile hamburger -->
          <button class="mobile-menu-btn" @click="mobileMenuOpen = !mobileMenuOpen">
            <span :class="{ open: mobileMenuOpen }"></span>
          </button>
        </div>
      </div>
    </header>

    <!-- Mobile Navigation Overlay -->
    <transition name="slide-right">
      <div v-if="mobileMenuOpen" class="mobile-nav-overlay" @click="mobileMenuOpen = false">
        <nav class="mobile-nav" @click.stop>
          <router-link to="/" @click="mobileMenuOpen = false">首页</router-link>
          <router-link to="/timeline" @click="mobileMenuOpen = false">时间线</router-link>
          <router-link to="/photos" @click="mobileMenuOpen = false">相册</router-link>
          <router-link to="/videos" @click="mobileMenuOpen = false">视频</router-link>
          <router-link to="/diaries" @click="mobileMenuOpen = false">日记</router-link>
          <router-link to="/search" @click="mobileMenuOpen = false">搜索</router-link>
          <div class="mobile-nav-divider"></div>
          <router-link v-if="!authStore.isLoggedIn" to="/login" @click="mobileMenuOpen = false">登录</router-link>
          <template v-else>
            <router-link to="/admin/photos" @click="mobileMenuOpen = false">后台管理</router-link>
            <a href="#" @click.prevent="handleLogout">退出登录</a>
          </template>
        </nav>
      </div>
    </transition>

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
const mobileMenuOpen = ref(false)

const handleScroll = () => {
  isScrolled.value = window.scrollY > 50
}

const handleCommand = (command) => {
  if (command === 'logout') {
    handleLogout()
  } else if (command === 'admin') {
    router.push('/admin')
  }
}

const handleLogout = () => {
  authStore.logout()
  mobileMenuOpen.value = false
  router.push('/')
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
    font-weight: 600;
    color: var(--text-primary);
    position: relative;
    text-shadow: 0 1px 2px rgba(255, 255, 255, 0.8);

    &.active, &:hover {
      color: var(--accent-color);
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

.mobile-menu-btn {
  display: none;
  width: 30px;
  height: 30px;
  background: none;
  border: none;
  cursor: pointer;
  position: relative;
  padding: 0;

  span, span::before, span::after {
    display: block;
    width: 24px;
    height: 2px;
    background: var(--text-primary);
    border-radius: 2px;
    transition: all 0.3s ease;
  }

  span::before, span::after {
    content: '';
    position: absolute;
    left: 3px;
  }

  span::before {
    top: 8px;
  }

  span::after {
    bottom: 8px;
  }

  span.open {
    background: transparent;

    &::before {
      top: 14px;
      transform: rotate(45deg);
    }

    &::after {
      bottom: 14px;
      transform: rotate(-45deg);
    }
  }
}

.mobile-nav-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.4);
  z-index: 999;

  .mobile-nav {
    position: absolute;
    right: 0;
    top: 0;
    bottom: 0;
    width: 260px;
    background: white;
    padding: 5rem 2rem 2rem;
    display: flex;
    flex-direction: column;
    gap: 1rem;
    box-shadow: -2px 0 8px rgba(0, 0, 0, 0.1);

    a {
      font-size: 1.1rem;
      padding: 0.5rem 0;
      color: var(--text-primary);
      font-weight: 500;
      transition: color 0.2s ease;

      &:hover, &.router-link-active {
        color: var(--primary-color);
      }
    }

    .mobile-nav-divider {
      height: 1px;
      background: rgba(0, 0, 0, 0.1);
      margin: 0.5rem 0;
    }
  }
}

.slide-right-enter-active,
.slide-right-leave-active {
  transition: opacity 0.3s ease;

  .mobile-nav {
    transition: transform 0.3s ease;
  }
}

.slide-right-enter-from,
.slide-right-leave-to {
  opacity: 0;

  .mobile-nav {
    transform: translateX(100%);
  }
}

.content {
  flex: 1;
  padding-top: 80px;
}

.footer {
  text-align: center;
  padding: 2rem;
  color: var(--text-secondary);
  font-size: 0.9rem;
}

@media (max-width: 768px) {
  .nav-links {
    display: none;
  }

  .actions .icon-btn,
  .actions .login-btn,
  .actions .user-menu {
    display: none;
  }

  .mobile-menu-btn {
    display: flex;
    align-items: center;
    justify-content: center;
  }
}
</style>
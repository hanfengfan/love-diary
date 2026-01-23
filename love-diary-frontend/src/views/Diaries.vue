<template>
  <div class="diaries">
    <div class="page-header">
      <h2>日记</h2>
    </div>

    <el-card>
      <div class="empty-state">
        <el-icon><Document /></el-icon>
        <p>日记功能开发中...</p>
      </div>
    </el-card>
  </div>
</template>

<script setup>
// 日记页面占位符
</script>

<style scoped>
.diaries {
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  margin-bottom: 20px;
}

.page-header h2 {
  margin: 0;
  color: #333;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 300px;
  color: #999;
}

.empty-state .el-icon {
  font-size: 48px;
  margin-bottom: 8px;
}
</style>
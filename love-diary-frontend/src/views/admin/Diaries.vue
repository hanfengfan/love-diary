<template>
  <div class="admin-diaries">
    <div class="page-header">
      <h2>日记管理</h2>
      <el-button type="primary">
        <el-icon><Plus /></el-icon>
        新建日记
      </el-button>
    </div>

    <el-card>
      <div class="empty-state">
        <el-icon><Document /></el-icon>
        <p>日记管理功能开发中...</p>
      </div>
    </el-card>
  </div>
</template>

<script setup>
// 日记管理页面占位符
</script>

<style scoped>
.admin-diaries {
  padding: 0;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
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
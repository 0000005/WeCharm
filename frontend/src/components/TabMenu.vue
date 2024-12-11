<script setup lang="ts">
import { ref } from 'vue'
import ChatInput from './ChatInput.vue'
import FriendsInfo from './FriendsInfo.vue'
import Settings from './Settings.vue'

const activeTab = ref('chat')
</script>

<template>
  <div class="tab-container">
    <el-tabs v-model="activeTab" class="tab-menu">
      <el-tab-pane label="聊天" name="chat">
        <template #label>
          <div class="custom-tab">
            <el-icon><ChatLineRound /></el-icon>
            <span>聊天</span>
          </div>
        </template>
        <div class="chat-content">
          <ChatInput />
        </div>
      </el-tab-pane>
      <el-tab-pane label="好友信息" name="friends">
        <template #label>
          <div class="custom-tab">
            <el-icon><UserFilled /></el-icon>
            <span>好友信息</span>
          </div>
        </template>
        <FriendsInfo />
      </el-tab-pane>
      <el-tab-pane label="设置" name="settings">
        <template #label>
          <div class="custom-tab">
            <el-icon><Setting /></el-icon>
            <span>设置</span>
          </div>
        </template>
        <Settings />
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<style scoped>
.tab-container {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.tab-menu {
  background-color: #fff;
  padding: 0 20px;
  border-bottom: 1px solid #e5e7eb;
}

.tab-menu :deep(.el-tabs__header) {
  margin-bottom: 0;
}

.tab-menu :deep(.el-tabs__nav-wrap::after) {
  height: 1px;
}

.custom-tab {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 15px;
}

.custom-tab .el-icon {
  font-size: 18px;
}

.chat-content {
  padding: 20px;
}
</style>
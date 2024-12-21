<script setup lang="ts">
import { ElMessage } from 'element-plus'
import { ref } from 'vue'
import type { ReplyCardMo } from '../model/ReplyMo'

interface Props {
  replyMo: ReplyCardMo
  isGenReplying: boolean
}

const props = defineProps<Props>()
const emit = defineEmits([ 'regenerate', 'send-success'])
const selectedReply = ref('')
const showButtons = ref(false)

const handleMouseEnter = () => {
  console.log('Mouse entered card')
  showButtons.value = true
}

const handleMouseLeave = () => {
  console.log('Mouse left card')
  showButtons.value = false
}

// 复制回复内容
const copyReply = async () => {
  if (selectedReply.value) {
    try {
      await navigator.clipboard.writeText(selectedReply.value)
      ElMessage.success('已复制到剪贴板')
    } catch (error) {
      console.error('复制失败:', error)
      ElMessage.error('复制失败')
    }
  }
}

// 直接回复
const sendReply = async () => {
  try {
    const response = await fetch('/api/weixin/send_msg', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ msg: selectedReply.value }),
    })
    
    if (response.ok) {
      ElMessage.success('发送成功')
      emit('send-success')
    } else {
      const data = await response.json()
      ElMessage.error(data.error || '发送失败')
    }
  } catch (error) {
    console.error('Error sending message:', error)
    ElMessage.error('发送失败')
  }
}
</script>

<template>
  <el-card 
    class="reply-card"
    @mouseenter="handleMouseEnter"
    @mouseleave="handleMouseLeave"
  >
    <template #header>
      <div class="card-header">
        <div class="context-info">
          <el-tag type="info" size="small" effect="plain">上下文数: {{ replyMo.contextNum }}</el-tag>
          <el-tag type="success" size="small" effect="plain" class="latest-msg">
            最近消息: {{ replyMo.lastMessage }}
          </el-tag>
        </div>
      </div>
    </template>
    <div class="reply-container">
      <!--回复列表-->
      <div class="reply-list">
        <el-radio-group v-model="selectedReply" class="reply-radio-group">
          <el-radio v-for="reply in replyMo.replyList" :key="reply" :label="reply" class="reply-radio-item">
            {{ reply }}
          </el-radio>
        </el-radio-group>
      </div>
      <div class="reply-btns" v-show="showButtons">
        <el-button type="primary" @click="sendReply" :disabled="!selectedReply">
          <el-icon>
            <Position />
          </el-icon>
          直接回复
        </el-button>
        <el-button @click="copyReply" :disabled="!selectedReply">
          <el-icon>
            <DocumentCopy />
          </el-icon>
          复制
        </el-button>
        <el-button @click="emit('regenerate')" :loading="isGenReplying">
          <el-icon>
            <RefreshRight />
          </el-icon>
          重新生成
        </el-button>
      </div>
    </div>
  </el-card>
</template>

<style scoped>
.reply-card {
  margin-bottom: 20px;
  position: relative;
  max-width: 900px;
  margin: 0 auto;
  margin-top: 20px;
}

.reply-container {
  
}

.reply-list {
  margin-bottom: 20px;
  padding: 0 20px;
}

.reply-radio-group {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.reply-radio-item {
  margin-right: 0;
  padding: 12px;
  border: 1px solid #dcdfe6;
  border-radius: 8px;
  height: auto;
  white-space: normal;
  line-height: 1.5;
}

.reply-radio-item :deep(.el-radio__label) {
  white-space: normal;
}

.reply-btns {
  display: flex;
  justify-content: center;
  gap: 12px;
  margin-top: 16px;
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.context-info {
  display: flex;
  gap: 12px;
  align-items: center;
}
.latest-msg {
  max-width: 300px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

</style>

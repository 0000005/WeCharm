<script setup lang="ts">
import { ref, watch } from 'vue'
import { ElMessage } from 'element-plus'

interface Intent {
  text: string;
}

interface Reply {
  style: string;
  text: string;
}

const inputText = ref('')
const intents = ref<string[]>([])
const selectedIntent = ref('')
const showIntentList = ref(false)
const replies = ref(['这是回复1这是回复1这是回复1这是回复1这是回复1这是回复1这是回复1这是回复1这是回复1这是回复1这是回复1这是回复1这是回复1这是回复1', '这是回复2', '这是回复3']) // 模拟回复列表
const selectedReply = ref('') // 选中的回复
const showReplyContainer = ref(false)
// 是否正在探索
const isExploring = ref(false)
// 是否正在生成回复
const isGenReplying = ref(false)

// 监听用户选择的意图
watch(selectedIntent, (newValue) => {
  if (newValue) {
    inputText.value = newValue
  }
})

const generateResponse = async () => {
  console.log('Generating response for:', inputText.value)
  try {
    if(isExploring.value) return
    isExploring.value = true
    const response = await fetch('/api/llm/intent')
    const data = await response.json()
    if (data.intent_list && Array.isArray(data.intent_list)) {
      intents.value = data.intent_list.map((intent: Intent) => intent.text)
      showIntentList.value = true
    } else {
      console.error('Invalid response format:', data)
      ElMessage.error("生成失败，格式错误！")
    }
  } catch (error) {
    ElMessage.error("生成失败，"+error)
    console.error('Error fetching intents:', error)
  } finally {
    isExploring.value = false
  }
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

// 重新生成回复
const regenerateReplies = () => {
  console.log('重新生成回复');
  handleSmartReply();
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
      showReplyContainer.value = false
      showIntentList.value = false
      inputText.value = ''
    } else {
      const data = await response.json()
      ElMessage.error(data.error || '发送失败')
    }
  } catch (error) {
    console.error('Error sending message:', error)
    ElMessage.error('发送失败，请稍后重试')
  }
}

// 返回上一步
const goBack = () => {
  showReplyContainer.value = false
}

// 处理智能回复按钮点击
const handleSmartReply = async () => {
  try {
    if(isGenReplying.value) return

    isGenReplying.value = true
    const response = await fetch('/api/llm/gen_reply', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        user_intent: inputText.value
      })
    })

    const data = await response.json()
    if (data.reply_list && Array.isArray(data.reply_list)) {
      replies.value = data.reply_list.map((reply: Reply) => reply.text)
      showReplyContainer.value = true
    } else {
      ElMessage.error("生成失败，格式错误")
      console.error('Invalid response format:', data)
    }
  } catch (error) {
    ElMessage.error("生成失败，"+error)
    console.error('Error generating replies:', error)
  } finally {
    isGenReplying.value = false
  }
}
</script>

<template>
  <div class="chat-input">
    <div class="brand-introduce">
      <p class="brand-name">微言妙语</p>
      <p class="brand-description">聪明的微信聊天助手，让你的每一次对话都滴水不漏、恰到好处！</p>
    </div>
    <!--回复配置页面-->
    <div class="chat-input-content" v-show="!showReplyContainer">
      <div class="intent-container">
        <!-- 意图列表 -->
        <div class="intent-list" v-if="showIntentList">
          <el-radio-group v-model="selectedIntent" class="intent-radio-group">
            <el-radio v-for="intent in intents" :key="intent" :label="intent">{{ intent }}</el-radio>
          </el-radio-group>
        </div>
        <!-- 意图输入框 -->
        <div class="intent-controler">
          <el-input v-model="inputText" placeholder="请输入你的回复内容（非必填），如：谢谢鉴赏" resize="none" clearable
            class="intent-input" />
          <el-button @click="generateResponse" class="generate-btn" :loading="isExploring" :disabled="isGenReplying">
            <el-icon>
              <Promotion />
            </el-icon>
            探索意图
          </el-button>
        </div>

      </div>

      <!-- <div class="controls-container">
        <div class="selectors">
          <el-select placeholder="请选择助手" class="selector">
            <el-option label="助手 1" value="1" />
            <el-option label="助手 2" value="2" />
          </el-select>
          <el-select placeholder="请选择风格" class="selector">
            <el-option label="正式" value="formal" />
            <el-option label="随意" value="casual" />
            <el-option label="幽默" value="humorous" />
          </el-select>
        </div>
      </div> -->

      <div class="smart-reply">
        <el-button type="primary" size="large" class="smart-reply-btn"
          :style="{ backgroundColor: '#2563eb', borderColor: '#2563eb' }" @click="handleSmartReply" :loading="isGenReplying" :disabled="isExploring">
          <el-icon>
            <Magic />
          </el-icon>
          智能回复
        </el-button>
      </div>
    </div>
    <!--回复选择容器-->
    <div class="reply-container" v-show="showReplyContainer">
      <!--回复列表-->
      <div class="reply-list">
        <el-radio-group v-model="selectedReply" class="reply-radio-group">
          <el-radio v-for="reply in replies" :key="reply" :label="reply" class="reply-radio-item">
            {{ reply }}
          </el-radio>
        </el-radio-group>
      </div>
      <div class="reply-btns">
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
        <el-button @click="regenerateReplies" :loading="isGenReplying" :disabled="isExploring">
          <el-icon>
            <RefreshRight />
          </el-icon>
          重新生成
        </el-button>
        <el-button @click="goBack">
          <el-icon>
            <Back />
          </el-icon>
          返回
        </el-button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.chat-input {
  background-color: #fff;
  border-top: 1px solid #e5e7eb;
}

.chat-input-content {
  max-width: 900px;
  margin: 0 auto;
  padding: 20px 0px;
}

.intent-container {
  display: flex;
  gap: 16px;
  align-items: stretch;
  border: 1px solid #dcdfe6;
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 16px;
  background-color: #fff;
  flex-direction: column;
  justify-content: flex-start;
}

.intent-controler {
  display: flex;
  flex-direction: row;
  flex: 1;
}

.intent-input {
  flex: 1;
}

.intent-input :deep(.el-textarea__inner) {
  border-radius: 8px;
  padding: 12px;
  font-size: 14px;
  height: 100%;
  background-color: #fcf9f9;
}

.intent-input :deep(.el-textarea__inner:focus) {
  background-color: #fff;
}

.generate-btn {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 14px 20px;
  font-size: 14px;
  border-radius: 6px;
  min-width: 120px;
  height: auto;
  align-self: center;
  margin-left: 10px;
}

.controls-container {
  display: flex;
  gap: 16px;
  justify-content: flex-start;
  align-items: center;
  margin-bottom: 16px;
}

.selectors {
  display: flex;
  gap: 12px;
  width: 100%;
}

.selector {
  width: 50%;
}

.selector :deep(.el-input__wrapper) {
  border-radius: 6px;
}

.el-radio {
  margin-right: 0;
}

.el-radio:deep(span) {
  word-break: break-all;
  white-space: normal;
}

/* .el-radio-group:deep(label) {
  padding-top: 15px;
  padding-bottom: 15px;
} */

.smart-reply {
  display: flex;
  justify-content: center;
  margin-bottom: 16px;
}

.smart-reply-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 0px;
  font-size: 16px;
  font-weight: 600;
  border-radius: 8px;
  transition: all 0.3s ease;
  width: 100%;
  max-width: 400px;
  justify-content: center;
  box-shadow: 0 2px 4px rgba(37, 99, 235, 0.1);
}

.smart-reply-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 6px rgba(37, 99, 235, 0.2);
  background-color: #1d4ed8 !important;
  border-color: #1d4ed8 !important;
}

.smart-reply-btn:active {
  transform: translateY(0);
  box-shadow: 0 2px 4px rgba(37, 99, 235, 0.1);
}

.smart-reply-btn .el-icon {
  font-size: 20px;
}

.brand-introduce {
  text-align: center;
  padding: 32px 20px;
  margin-top: 24px;
  background: linear-gradient(135deg, #f0f7ff 0%, #ffffff 100%);
  border-radius: 16px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

.brand-name {
  font-size: 2.5rem;
  font-weight: 600;
  color: #2563eb;
  margin: 0 0 16px 0;
  letter-spacing: 0.05em;
  background: linear-gradient(to right, #2563eb, #3b82f6);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
}

.brand-description {
  font-size: 1.125rem;
  color: #4b5563;
  line-height: 1.6;
  max-width: 600px;
  margin: 0 auto;
}

.intent-list {
  min-width: 200px;
  padding: 8px;
}

.intent-radio-group {
  display: flex;
  flex-direction: column;
  gap: 12px;
  text-align: left;
  align-items: baseline;
}

.reply-container {
  padding-top: 20px;
  padding-bottom: 20px;
}

.reply-list {
  margin-bottom: 20px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 20px;
  ;
}

.reply-radio-group {
  display: flex;
  flex-direction: column;
  gap: 12px;
  width: 100%;
  align-items: baseline;
}

.reply-radio-item {
  padding: 12px;
  border-radius: 6px;
  background-color: white;
  transition: all 0.3s ease;
}

.reply-radio-item:hover {
  border-color: #2563eb;
  background-color: #f0f7ff;
}

.reply-btns {
  display: flex;
  gap: 12px;
  justify-content: center;
}

.reply-btns .el-button {
  display: flex;
  align-items: center;
  gap: 4px;
}
</style>
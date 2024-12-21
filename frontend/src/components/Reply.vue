<script setup lang="ts">
import { ref, watch, inject, type Ref } from 'vue'
import { ElMessage } from 'element-plus'
import ReplyItem from './ReplyItem.vue'
import type { ReplyCardMo,ReplyListItem } from '../model/ReplyMo'

// 注入全局会话列表
const sessionList = inject<Ref<ReplyCardMo[]>>('sessionList')

const inputText = ref('')
const selectedIntent = ref('')
const showReplyContainer = ref(false)

// 是否正在生成回复
const isGenReplying = ref(false)

// 监听用户选择的意图
watch(selectedIntent, (newValue) => {
  if (newValue) {
    inputText.value = newValue
    handleSmartReply()
  }
})

// 重新生成回复
const regenerateReplies = () => {
  console.log('重新生成回复');
  handleSmartReply();
}

// 处理智能回复按钮点击
const handleSmartReply = async () => {
  try {
    if (isGenReplying.value) return

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

    if (!response.ok) {
      const errorData = await response.json()
      ElMessage.error(errorData.error)
      return
    }

    const data = await response.json()
    if (data.replyList && Array.isArray(data.replyList)) {
      const replyList = data.replyList.map((reply: ReplyListItem) => reply.text)

      // 构造一个 ReplyCardMo 对象
      const replyCardMo: ReplyCardMo = {
        //随机生成id
        id: Math.floor(Math.random() * 1000000),
        contextNum: data.contextNum,
        lastMessage: data.lastMessage,
        userIntent: inputText.value,
        replyList: replyList,
        wechatNickname:data.wechatNickname
      }
      sessionList?.value.push(replyCardMo)
      showReplyContainer.value = true
    } else {
      ElMessage.error("生成失败，格式错误")
      console.error('Invalid response format:', data)
    }
  } catch (error) {
    ElMessage.error("生成失败，" + error)
    console.error('Error generating replies:', error)
  } finally {
    isGenReplying.value = false
    inputText.value = ''
  }
}

const handleSendSuccess = () => {
  inputText.value = ''
}
</script>

<template>
  <div class="chat-input">
    <!--默认首页  -->
    <div v-show="!showReplyContainer">
      <div class="brand-introduce">
        <p class="brand-name">微言妙语</p>
        <p class="brand-description">聪明的微信聊天助手，让你的每一次对话都滴水不漏、恰到好处！</p>
      </div>
      <!--回复配置页面-->
      <div class="chat-input-content" v-show="!showReplyContainer">
        <div class="intent-container">
          <!-- 意图输入框 -->
          <div class="intent-controler">
            <el-input v-model="inputText" placeholder="请输入你的回复内容（非必填），如：表达感谢" resize="none" clearable
              class="intent-input" />
          </div>
        </div>

        <div class="smart-reply">
          <el-button type="primary" size="large" class="smart-reply-btn" @click="handleSmartReply"
            :loading="isGenReplying">
            <el-icon>
              <Magic />
            </el-icon>
            智能回复
          </el-button>
        </div>
      </div>
    </div>

    <!--回复选择容器-->
    <div v-show="showReplyContainer">
      <ReplyItem 
        v-for="session in sessionList"
        :key="session.id"
        :replyMo="session"
        :isGenReplying="isGenReplying"
        @send-success="handleSendSuccess"
        @regenerate="regenerateReplies" 
      />
    </div>

    <div v-show="showReplyContainer" class="bottom-fixed-intent-input">
      <div class="intent-controler">
        <el-input v-model="inputText" placeholder="请输入你的回复内容（非必填），如：表达感谢" resize="none" clearable
          class="intent-input" />
      </div>
      <div class="smart-reply">
        <el-button type="primary" size="large" class="smart-reply-btn" @click="handleSmartReply"
          :loading="isGenReplying">
          <el-icon>
            <Magic />
          </el-icon>
          智能回复
        </el-button>
      </div>
    </div>

  </div>
</template>

<style scoped>
.chat-input {
  background-color: #fff;
  border-top: 1px solid #e5e7eb;
  padding-top: 20px;
  padding-bottom: 20px;
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
  color: #666;
  line-height: 1.6;
  max-width: 600px;
  margin: 0 auto;
  margin-top: 8px;
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

.bottom-fixed-intent-input {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background-color: #fff;
  padding: 16px;
  border-top: 1px solid #e5e7eb;
  display: flex;
  gap: 16px;
  align-items: center;
  z-index: 1000;
}

.bottom-fixed-intent-input .intent-controler {
  flex: 1;
}

.bottom-fixed-intent-input .smart-reply-btn {
  white-space: nowrap;
}
</style>
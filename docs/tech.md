### 自动生成的逻辑
#### 为什么需要自动生成功能
- 减少操作步骤，提高软件的利用率

#### 自动生成的时机
- 当微信聊天窗口激活
- 当好友设置的自动生成开关打开
- 当发现接收到了新消息时
- 当前好友不处于正在生成的状态

#### 自动生成的逻辑
- 回复页面的回复内容应该是流式的，不是一次性的

#### 自动生成的技术细节
- 如何让前端感知到好友切换？
  - SSE？
  - WebSocket？

- 后端需要通知前端哪些信息？
  - 好友切换
  - 有新消息



### 其他想法
回复页面是和好友强相关的，这意味着不同的好友，对应不同的回复页面。 每次回复的内容都保存在内存中。
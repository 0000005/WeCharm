//回复列表的模型
export interface ReplyCardMo {
    //id
    id: number
    //用户昵称
    wechatNickname: string,
    //回复内容数组
    replyList: string[]
    //上下文数
    contextNum: number
    //用户意图
    userIntent: string
    //用户最新收到的消息
    lastMessage: string
}

// 回复列表
export interface ReplyListItem {
    style: string;
    text: string;
  }
  
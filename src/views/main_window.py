# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 4.2.1-0-g80c4cb6)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import gettext
import traceback
import threading
import pythoncom
from wxauto import WeChat
from utils.weixin_utils import WeixinUtils
from utils.llm_utils import LLMUtils

_ = gettext.gettext

###########################################################################
## Class main_frame
###########################################################################


class main_frame(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(
            self,
            parent,
            id=wx.ID_ANY,
            title="微信聊天助手",
            pos=wx.DefaultPosition,
            size=wx.Size(500, 800),
            style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL,
        )

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        content_sizer = wx.BoxSizer(wx.VERTICAL)

        self.assistant_label = wx.StaticText(
            self,
            wx.ID_ANY,
            _("选择聊天助手"),
            wx.DefaultPosition,
            wx.Size(500, -1),
            0,
        )
        self.assistant_label.Wrap(-1)
        content_sizer.Add(self.assistant_label, 0, wx.ALL, 5)

        assistant_choices = ["通用", "非暴力沟通"]
        self.assistant_combo = wx.ComboBox(
            self,
            wx.ID_ANY,
            "通用",
            wx.DefaultPosition,
            wx.Size(500, -1),
            assistant_choices,
            0,
        )
        content_sizer.Add(self.assistant_combo, 0, wx.ALL, 5)

        self.m_staticText2 = wx.StaticText(
            self, wx.ID_ANY, _("关系"), wx.DefaultPosition, wx.DefaultSize, 0
        )
        self.m_staticText2.Wrap(-1)

        content_sizer.Add(self.m_staticText2, 0, wx.ALL, 5)

        self.relation_input = wx.TextCtrl(
            self, wx.ID_ANY, wx.EmptyString, wx.Point(-1, -1), wx.Size(500, -1), 0
        )
        content_sizer.Add(self.relation_input, 0, wx.ALL, 5)

        self.user_intent_label = wx.StaticText(
            self,
            wx.ID_ANY,
            _("请输入你的意图"),
            wx.DefaultPosition,
            wx.Size(500, -1),
            0,
        )
        self.user_intent_label.Wrap(-1)

        content_sizer.Add(self.user_intent_label, 0, wx.ALL, 5)

        self.user_intent_input = wx.TextCtrl(
            self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(500, -1), 0
        )
        content_sizer.Add(self.user_intent_input, 0, wx.ALL, 5)

        reply_button_sizer = wx.GridSizer(0, 3, 0, 0)

        self.generate_intent_btn = wx.Button(
            self, wx.ID_ANY, _("生成意图"), wx.DefaultPosition, wx.DefaultSize, 0
        )
        reply_button_sizer.Add(
            self.generate_intent_btn,
            0,
            wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL,
            5,
        )

        self.generate_btn = wx.Button(
            self, wx.ID_ANY, _("生成回复"), wx.DefaultPosition, wx.DefaultSize, 0
        )
        reply_button_sizer.Add(
            self.generate_btn,
            0,
            wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL,
            5,
        )

        self.clear_btn = wx.Button(
            self, wx.ID_ANY, _("清空"), wx.DefaultPosition, wx.DefaultSize, 0
        )
        reply_button_sizer.Add(
            self.clear_btn,
            0,
            wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL,
            5,
        )

        content_sizer.Add(reply_button_sizer, 0, wx.EXPAND, 5)

        replay_sizer = wx.BoxSizer(wx.VERTICAL)

        reply_list_radioChoices = []
        self.reply_list_radio = wx.RadioBox(
            self,
            wx.ID_ANY,
            _("回复建议列表"),
            wx.DefaultPosition,
            wx.Size(500, -1),
            reply_list_radioChoices,
            1,
            wx.RA_SPECIFY_COLS,
        )
        replay_sizer.Add(self.reply_list_radio, 0, wx.ALL, 5)

        content_sizer.Add(replay_sizer, 1, wx.EXPAND, 5)

        operation_sizer = wx.GridSizer(0, 2, 0, 0)

        self.send_directly_btn = wx.Button(
            self, wx.ID_ANY, _("直接发送"), wx.DefaultPosition, wx.DefaultSize, 0
        )
        operation_sizer.Add(self.send_directly_btn, 0, wx.ALL, 5)

        self.copy_btn = wx.Button(
            self, wx.ID_ANY, _("复制"), wx.DefaultPosition, wx.DefaultSize, 0
        )
        operation_sizer.Add(self.copy_btn, 0, wx.ALL, 5)

        content_sizer.Add(operation_sizer, 0, wx.EXPAND, 5)

        self.SetSizer(content_sizer)
        self.Layout()  # Explicit Layout() call

        self.Centre(wx.BOTH)

        # Hide controls initially
        self.hide_operation_controls()

        # Bind events
        self.generate_btn.Bind(wx.EVT_BUTTON, self.on_generate_btn_click)
        self.generate_intent_btn.Bind(wx.EVT_BUTTON, self.on_generate_intent_btn_click)
        self.copy_btn.Bind(wx.EVT_BUTTON, self.on_copy_btn_click)
        self.send_directly_btn.Bind(wx.EVT_BUTTON, self.on_send_directly_btn_click)
        self.clear_btn.Bind(wx.EVT_BUTTON, self.on_clear_btn_click)
        self.assistant_combo.Bind(wx.EVT_COMBOBOX, self.on_assistant_select)

        self.llm_utils = LLMUtils()
        self.weixin_utils = WeixinUtils()
        self.is_generating = False
        self.current_thread = None
        self.selected_assistant = "通用"  # 默认使用通用助手

    def __del__(self):
        pass

    def on_send_directly_btn_click(self, event):
        """Handle send directly button click event"""
        try:
            # Get selected radio box value
            selection = self.reply_list_radio.GetSelection()
            if selection != wx.NOT_FOUND:
                selected_text = self.reply_list_radio.GetString(selection)
                if selected_text:
                    # Send message via WeChat
                    wx_instance = WeChat()
                    wx_instance.SendMsg(msg=selected_text)
                else:
                    wx.MessageBox("请选择要发送的回复", "提示", wx.OK | wx.ICON_WARNING)
            else:
                wx.MessageBox("请选择要发送的回复", "提示", wx.OK | wx.ICON_WARNING)
        except Exception as e:
            print(f"发送消息时发生错误：{traceback.format_exc()}")
            wx.MessageBox(
                f"发送消息时发生错误：{str(e)}", "错误", wx.OK | wx.ICON_ERROR
            )

        event.Skip()

    def on_copy_btn_click(self, event):
        """Handle copy button click event"""
        try:
            # Get selected radio box value
            selection = self.reply_list_radio.GetSelection()
            if selection != wx.NOT_FOUND:
                selected_text = self.reply_list_radio.GetString(selection)
                if selected_text:
                    # Copy to clipboard
                    if wx.TheClipboard.Open():
                        wx.TheClipboard.SetData(wx.TextDataObject(selected_text))
                        wx.TheClipboard.Close()
        except Exception as e:
            print(f"复制文本时发生错误：{traceback.format_exc()}")
            wx.MessageBox(
                f"复制文本时发生错误：{str(e)}", "错误", wx.OK | wx.ICON_ERROR
            )

        event.Skip()

    def restore_generate_button(self):
        """Restore the generate button to its original state"""
        self.generate_btn.Enable()
        self.generate_btn.SetLabel(_("生成回复"))

    def show_operation_controls(self):
        """Show the reply list radio box and operation buttons"""
        self.reply_list_radio.Show()
        self.send_directly_btn.Show()
        self.copy_btn.Show()
        self.Layout()

    def hide_operation_controls(self):
        """Hide the reply list radio box and operation buttons"""
        self.reply_list_radio.Hide()
        self.send_directly_btn.Hide()
        self.copy_btn.Hide()
        self.Layout()

    def on_generate_btn_click(self, event):
        """Handle generate button click event"""
        # Show loading state
        self.generate_btn.Disable()
        self.generate_btn.SetLabel(_("生成中..."))
        # Hide operation controls
        self.hide_operation_controls()

        # Get user inputs
        user_intent = self.user_intent_input.GetValue()
        relationship = self.relation_input.GetValue()

        # Validate inputs
        if not user_intent:
            wx.MessageBox("请输入你的意图", "错误", wx.OK | wx.ICON_ERROR)
            self.restore_generate_button()
            return

        # Start worker thread
        worker_thread = threading.Thread(
            target=self._generate_response_worker, args=(user_intent, relationship)
        )
        worker_thread.daemon = True
        worker_thread.start()

        event.Skip()

    def _generate_response_worker(self, user_intent, relationship):
        """Worker thread function to handle time-consuming operations"""
        try:
            # Initialize COM in the worker thread
            pythoncom.CoInitialize()

            # Get chat history
            chat_history = WeixinUtils.get_chat_history(40)

            # Get LLM response
            response = LLMUtils.get_llm_response(
                prompt_type=self.selected_assistant,
                user_intent=user_intent,
                chat_history=chat_history,
                relationship=relationship,
            )

            # Update UI in main thread
            wx.CallAfter(self._update_ui_with_response, response)

        except Exception as e:
            print(f"生成回复时发生错误：{traceback.format_exc()}")
            error_msg = f"生成回复时发生错误：{str(e)}"
            wx.CallAfter(wx.MessageBox, error_msg, "错误", wx.OK | wx.ICON_ERROR)
        finally:
            # Uninitialize COM
            pythoncom.CoUninitialize()
            wx.CallAfter(self.restore_generate_button)

    def _update_ui_with_response(self, response):
        """Update UI with the generated response"""
        try:
            # Update radio box choices with responses
            choices = [f"{resp.text}" for resp in response.suggested_response]
            # Create a new RadioBox with updated choices
            old_radio = self.reply_list_radio
            self.reply_list_radio = wx.RadioBox(
                self,
                wx.ID_ANY,
                _("回复建议列表"),
                wx.DefaultPosition,
                wx.Size(500, -1),
                choices,
                1,
                wx.RA_SPECIFY_COLS,
            )

            # Get the replay_sizer
            replay_sizer = old_radio.GetContainingSizer()
            if replay_sizer:
                # Remove old radio box
                replay_sizer.Detach(old_radio)
                old_radio.Destroy()
                # Add new radio box
                replay_sizer.Add(self.reply_list_radio, 0, wx.ALL, 5)
                replay_sizer.Layout()

            # Show controls after generating suggestions
            self.show_operation_controls()

        except Exception as e:
            print(f"更新UI时发生错误：{traceback.format_exc()}")
            error_msg = f"更新UI时发生错误：{str(e)}"
            wx.MessageBox(error_msg, "错误", wx.OK | wx.ICON_ERROR)

    def on_clear_btn_click(self, event):
        """Handle clear button click event"""
        self.hide_operation_controls()
        self.user_intent_input.SetValue("")
        if hasattr(self, "intent_list_radio"):
            self.intent_list_radio.Hide()

    def on_assistant_select(self, event):
        """当选择不同的助手时触发"""
        self.selected_assistant = self.assistant_combo.GetValue()

    def on_generate_intent_btn_click(self, event):
        """Handle generate intent button click event"""
        if self.is_generating:
            return

        self.is_generating = True
        self.generate_intent_btn.SetLabel(_("生成中..."))
        self.generate_intent_btn.Disable()

        relationship = self.relation_input.GetValue()

        # Create and start the worker thread
        self.current_thread = threading.Thread(
            target=self._generate_intent_worker, args=(relationship,)
        )
        self.current_thread.start()

    def _generate_intent_worker(self, relationship):
        """Worker thread function to handle intent generation"""
        try:
            pythoncom.CoInitialize()
            # Get chat history
            chat_history = WeixinUtils.get_chat_history(40)

            response = self.llm_utils.get_llm_response_no_intent(
                prompt_type="生成意图",
                chat_history=chat_history,
                relationship=relationship,
            )
            wx.CallAfter(self._update_intent_list, response)
        except Exception as e:
            wx.CallAfter(
                wx.MessageBox,
                f"生成意图时发生错误：{str(e)}\n{traceback.format_exc()}",
                "错误",
                wx.OK | wx.ICON_ERROR,
            )
        finally:
            pythoncom.CoUninitialize()
            wx.CallAfter(self._restore_intent_button)

    def _update_intent_list(self, response):
        """Update UI with the generated intents"""
        if not response or not response.intent_list:
            wx.MessageBox("未能生成有效的意图", "提示", wx.OK | wx.ICON_INFORMATION)
            return

        content_sizer = self.GetSizer()

        # First check if we have an existing intent_list_radio to destroy
        if hasattr(self, "intent_list_radio"):
            try:
                self.intent_list_radio.Hide()
                self.intent_list_radio.Destroy()
            except:
                pass  # If already destroyed, just continue

        # Remove any existing static box sizer
        for i in range(content_sizer.GetItemCount() - 1, -1, -1):
            item = content_sizer.GetItem(i)
            if (
                item
                and item.GetSizer()
                and isinstance(item.GetSizer(), wx.StaticBoxSizer)
            ):
                try:
                    sizer = item.GetSizer()
                    if sizer.GetStaticBox().GetLabel() == _("快捷意图列表"):
                        sizer.Clear(True)  # This will safely destroy all children
                        content_sizer.Remove(i)
                        break
                except:
                    pass  # If already destroyed, just continue

        # Create a new ListBox with the updated intents
        self.intent_list_radio = wx.ListBox(
            self,
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.Size(500, 100),
            [intent.text for intent in response.intent_list if intent.text.strip()],
            wx.LB_SINGLE | wx.LB_NEEDED_SB,
        )

        # Create a static box to group the ListBox
        static_box = wx.StaticBox(self, wx.ID_ANY, _("快捷意图列表"))
        static_box_sizer = wx.StaticBoxSizer(static_box, wx.VERTICAL)
        static_box_sizer.Add(self.intent_list_radio, 1, wx.ALL | wx.EXPAND, 5)

        # Bind the selection event
        self.intent_list_radio.Bind(wx.EVT_LISTBOX, self.on_intent_select)

        # Insert the new ListBox after user_intent_input (at index 6)
        content_sizer.Insert(6, static_box_sizer, 0, wx.ALL | wx.EXPAND, 5)

        self.intent_list_radio.Show()
        self.Layout()

    def on_intent_select(self, event):
        """Handle intent selection event"""
        selected_index = self.intent_list_radio.GetSelection()
        if selected_index != -1:
            selected_text = self.intent_list_radio.GetString(selected_index)
            print(f"Selected text: {selected_text}")  # Debug log
            self.user_intent_input.SetValue(selected_text)
            # Optionally, you can also set focus to the input
            self.user_intent_input.SetFocus()

    def _restore_intent_button(self):
        """Restore the generate intent button to its original state"""
        self.is_generating = False
        self.generate_intent_btn.SetLabel(_("生成意图"))
        self.generate_intent_btn.Enable()

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
            title=wx.EmptyString,
            pos=wx.DefaultPosition,
            size=wx.Size(500, 550),
            style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL,
        )

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        content_sizer = wx.BoxSizer(wx.VERTICAL)

        self.user_intent_label = wx.StaticText(
            self,
            wx.ID_ANY,
            _("请输入你表达的意思"),
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

        self.m_staticText2 = wx.StaticText(
            self, wx.ID_ANY, _("关系"), wx.DefaultPosition, wx.DefaultSize, 0
        )
        self.m_staticText2.Wrap(-1)

        content_sizer.Add(self.m_staticText2, 0, wx.ALL, 5)

        self.relation_input = wx.TextCtrl(
            self, wx.ID_ANY, wx.EmptyString, wx.Point(-1, -1), wx.Size(500, -1), 0
        )
        content_sizer.Add(self.relation_input, 0, wx.ALL, 5)

        reply_button_sizer = wx.GridSizer(0, 2, 0, 0)

        self.generate_btn = wx.Button(
            self, wx.ID_ANY, _("生成回复"), wx.DefaultPosition, wx.DefaultSize, 0
        )
        reply_button_sizer.Add(self.generate_btn, 0, wx.ALL, 5)

        self.clear_btn = wx.Button(
            self, wx.ID_ANY, _("清空"), wx.DefaultPosition, wx.DefaultSize, 0
        )
        reply_button_sizer.Add(self.clear_btn, 0, wx.ALL, 5)

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

        content_sizer.Add(replay_sizer, 0, wx.EXPAND, 5)

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
        self.Layout()

        self.Centre(wx.BOTH)

        # Hide controls initially
        self.hide_operation_controls()

        # Bind events
        self.generate_btn.Bind(wx.EVT_BUTTON, self.on_generate_btn_click)
        self.copy_btn.Bind(wx.EVT_BUTTON, self.on_copy_btn_click)
        self.send_directly_btn.Bind(wx.EVT_BUTTON, self.on_send_directly_btn_click)
        self.clear_btn.Bind(wx.EVT_BUTTON, self.on_clear_btn_click)

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
            wx.MessageBox("请输入你表达的意思", "错误", wx.OK | wx.ICON_ERROR)
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
            chat_history = WeixinUtils.get_chat_history()

            # Get LLM response
            response = LLMUtils.get_llm_response(
                prompt_type="通用",
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
            # Replace the old RadioBox with the new one in the sizer
            old_radio_sizer = old_radio.GetContainingSizer()
            old_radio_sizer.Replace(old_radio, self.reply_list_radio)
            old_radio.Destroy()

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

# -*- mode: python ; coding: utf-8 -*-

import sys
import os
from pathlib import Path

block_cipher = None

# 获取项目根目录
PROJ_PATH = Path(os.path.abspath(os.path.dirname('.')))
BACKEND_SRC_PATH = PROJ_PATH / 'src'
BACKEND_STATIC_PATH = PROJ_PATH / 'static'
BACKEND_LOGO_PATH = PROJ_PATH / 'logo.png'

a = Analysis(
    [str(BACKEND_SRC_PATH / 'gui.py')],
    pathex=[str(PROJ_PATH)],
    binaries=[],
    datas=[
        (str(BACKEND_SRC_PATH),"backend/src"),
        (str(BACKEND_STATIC_PATH),"backend/static"),
        (str(BACKEND_LOGO_PATH),"backend"),
    ],
    hiddenimports=[
        'win32gui', 
        'win32con', 
        'webview',
        'webview.platforms.winforms',
        'pythoncom',
        'win32api',
        'win32com.client',
        'win32com.client.gencache',
        'win32com.client.dynamic',
        'clr',
        'clr_loader',
        'System.Windows.Forms',
        'System.Drawing',
        'flask',
        'flask_cors',
        'werkzeug',
        'jinja2',
        'itsdangerous',
        'click',
        'wxauto',
        'langchain_openai',
        'pydantic',
        'pydantic.deprecated',
        'pydantic.deprecated.decorator',
        'pydantic.json',
        'pydantic.networks',
        'pydantic.types',
        'pydantic.fields',
        'pydantic.main',
        'pydantic.error_wrappers',
        'pydantic.utils',
        'pydantic.errors',
        'pydantic.validators',
        'pydantic.datetime_parse',
        'pydantic.class_validators',
        'pydantic.parse',
        'pydantic.schema',
        'pydantic.typing',
        'pydantic.version',
        'pydantic.config',
        'pydantic.env_settings',
        'pydantic.tools',
        'pydantic.mypy',
        'pydantic.generics',
        'pydantic.dataclasses',
        'pydantic.decorator',
        'pydantic.color',
        'pydantic.networks',
        'pydantic.paths',
        'pydantic.types',
        'logging.config',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    exclude_datas=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='wecharm',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=str(PROJ_PATH / 'logo.png')
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    a.scripts,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='WeCharm',
)

# -*- mode: python -*-

block_cipher = None


a = Analysis(['launcher.py'],
             pathex=['/Users/yzhou/Documents/PersonalProject/Sleep-Early'],
             binaries=[],
             datas=[('/Users/yzhou/Documents/PersonalProject/Sleep-Early/images','./images'),
             ('/Users/yzhou/Documents/PersonalProject/Sleep-Early/iproxy','.')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='Sleep Early',
          debug=False,
          strip=False,
          upx=True,
          console=False , icon='icon.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='launcher')
app = BUNDLE(coll,
             name='Sleep Early.app',
             icon='icon.icns',
             bundle_identifier=None,
             info_plist={'CFBundleShortVersionString': '1.0.1',
             'NSHighResolutionCapable': 'True'})

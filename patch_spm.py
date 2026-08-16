import re, os

# 1. Fix CanaryAppIcon -> AppIcon
pbxproj = 'ios/Runner.xcodeproj/project.pbxproj'
if os.path.exists(pbxproj):
    with open(pbxproj, 'r') as f:
        content = f.read()
    content = content.replace('ASSETCATALOG_COMPILER_APPICON_NAME = CanaryAppIcon', 'ASSETCATALOG_COMPILER_APPICON_NAME = AppIcon')
    with open(pbxproj, 'w') as f:
        f.write(content)
    print('Fixed CanaryAppIcon -> AppIcon')

print('Done: pbxproj patched')

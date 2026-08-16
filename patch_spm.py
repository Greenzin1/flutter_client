import re, os

# 1. Strip ALL SPM from pbxproj
pbxproj = 'ios/Runner.xcodeproj/project.pbxproj'
with open(pbxproj, 'r') as f:
    content = f.read()

content = re.sub(
    r'/\* Begin XCLocalSwiftPackageReference section \*/.*?/\* End XCLocalSwiftPackageReference section \*/',
    '/* removed */', content, flags=re.DOTALL
)
content = re.sub(
    r'/\* Begin XCSwiftPackageProductDependency section \*/.*?/\* End XCSwiftPackageProductDependency section \*/',
    '/* removed */', content, flags=re.DOTALL
)
content = re.sub(r'\t\t\tpackageReferences = \([^)]*\);\n', '', content, flags=re.DOTALL)
content = re.sub(r'\t\t\tpackageProductDependencies = \([^)]*\);', '', content, flags=re.DOTALL)
content = re.sub(r'\t+\w+ /\* FlutterGeneratedPluginSwiftPackage in Frameworks \*/,\n', '', content)

with open(pbxproj, 'w') as f:
    f.write(content)
print('SPM stripped from pbxproj')

# 2. Remove Package.resolved files
for root, dirs, files in os.walk('ios'):
    for fname in files:
        if fname == 'Package.resolved':
            os.remove(os.path.join(root, fname))
print('Package.resolved files removed')

# 3. Comment out import receive_sharing_intent and usage in SceneDelegate
scene = 'ios/Runner/SceneDelegate.swift'
if os.path.exists(scene):
    with open(scene, 'r') as f:
        content = f.read()
    content = content.replace('import receive_sharing_intent', '// import receive_sharing_intent')
    content = content.replace('ReceiveSharingIntentPlugin.instance.scene(', '// ReceiveSharingIntentPlugin.instance.scene(')
    content = content.replace('ReceiveSharingIntentPlugin.instance.scene(scene, openURLContexts:', '// ReceiveSharingIntentPlugin.instance.scene(scene, openURLContexts:')
    with open(scene, 'w') as f:
        f.write(content)
    print(f'Patched {scene}')

# 4. Stub ShareViewController (remove SPM dependency)
share_ext = 'ios/ShareExtension/ShareViewController.swift'
if os.path.exists(share_ext):
    stub = (
        "import UIKit\n"
        "\n"
        "class ShareViewController: UIViewController {\n"
        "    override func viewDidLoad() {\n"
        "        super.viewDidLoad()\n"
        "        self.extensionContext?.completeRequest(returningItems: [], completionHandler: nil)\n"
        "    }\n"
        "}\n"
    )
    with open(share_ext, 'w') as f:
        f.write(stub)
    print(f'Replaced {share_ext}')

print('Done: SPM stripped, Swift patched')

# 5. Fix CanaryAppIcon -> AppIcon
with open(pbxproj, 'r') as f:
    content = f.read()
content = content.replace('ASSETCATALOG_COMPILER_APPICON_NAME = CanaryAppIcon', 'ASSETCATALOG_COMPILER_APPICON_NAME = AppIcon')
with open(pbxproj, 'w') as f:
    f.write(content)
print('Fixed CanaryAppIcon -> AppIcon')

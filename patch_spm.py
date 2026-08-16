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

# 3. Rewrite SceneDelegate (remove receive_sharing_intent dependency)
scene = 'ios/Runner/SceneDelegate.swift'
minimal_scene = """import Flutter
import UIKit

class SceneDelegate: FlutterSceneDelegate {
}
"""
with open(scene, 'w') as f:
    f.write(minimal_scene)
print(f'Rewrote {scene} with minimal stub')

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

# 6. Comment out import WebRTC in AppDelegate
app_delegate = 'ios/Runner/AppDelegate.swift'
if os.path.exists(app_delegate):
    with open(app_delegate, 'r') as f:
        content = f.read()
    content = content.replace('import WebRTC', '// import WebRTC')
    content = re.sub(r'^(\s*)let rtc = RTCAudioSession\.sharedInstance\(\)', r'\1// let rtc = RTCAudioSession.sharedInstance()', content, flags=re.MULTILINE)
    content = re.sub(r'^(\s*)rtc\.', r'\1// rtc.', content, flags=re.MULTILINE)
    with open(app_delegate, 'w') as f:
        f.write(content)
    print(f'Patched {app_delegate}')

# 7. Rewrite AppDelegate to remove ALL SPM dependencies
minimal_appdelegate = """import Flutter
import UIKit

@main
@objc class AppDelegate: FlutterAppDelegate {
  override func application(
    _ application: UIApplication,
    didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?
  ) -> Bool {
    GeneratedPluginRegistrant.register(with: self)
    return super.application(application, didFinishLaunchingWithOptions: launchOptions)
  }
}
"""
with open(app_delegate, 'w') as f:
    f.write(minimal_appdelegate)
print(f'Rewrote {app_delegate} with minimal stub')

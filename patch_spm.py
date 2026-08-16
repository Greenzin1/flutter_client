import re, os

# 1. Rewrite SceneDelegate (remove receive_sharing_intent dependency)
scene = 'ios/Runner/SceneDelegate.swift'
minimal_scene = """import Flutter
import UIKit

class SceneDelegate: FlutterSceneDelegate {
}
"""
with open(scene, 'w') as f:
    f.write(minimal_scene)
print(f'Rewrote {scene}')

# 2. Stub ShareViewController
share_ext = 'ios/ShareExtension/ShareViewController.swift'
if os.path.exists(share_ext):
    stub = """import UIKit

class ShareViewController: UIViewController {
    override func viewDidLoad() {
        super.viewDidLoad()
        self.extensionContext?.completeRequest(returningItems: [], completionHandler: nil)
    }
}
"""
    with open(share_ext, 'w') as f:
        f.write(stub)
    print(f'Replaced {share_ext}')

# 3. Minimal AppDelegate
app_delegate = 'ios/Runner/AppDelegate.swift'
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
print(f'Rewrote {app_delegate}')

# 4. Fix CanaryAppIcon -> AppIcon
pbxproj = 'ios/Runner.xcodeproj/project.pbxproj'
if os.path.exists(pbxproj):
    with open(pbxproj, 'r') as f:
        content = f.read()
    content = content.replace('ASSETCATALOG_COMPILER_APPICON_NAME = CanaryAppIcon', 'ASSETCATALOG_COMPILER_APPICON_NAME = AppIcon')
    with open(pbxproj, 'w') as f:
        f.write(content)
    print('Fixed CanaryAppIcon -> AppIcon')

print('Done: Swift files patched')

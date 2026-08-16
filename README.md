# Fluxer iOS (Unsigned IPA)

This is a fork of the [Fluxer Flutter client](https://github.com/fluxerapp/flutter_client) that builds **unsigned IPA files** via GitHub Actions for sideloading on iOS using [Feather](https://github.com/nicholaostr/feather) or similar tools.

## Why does this fork exist?

The Fluxer iOS app is only distributed through **TestFlight**, which is limited to **Plutonium subscribers** (Fluxer's premium tier). If you don't have Plutonium, there's no way to install the native iOS app.

This fork uses GitHub Actions to build the same open source Flutter client as an **unsigned IPA** that you can sideload onto your iPhone using Feather or any other signing tool. No jailbreak required.

## How to install

1. Download the latest IPA from [Actions](https://github.com/Greenzin1/flutter_client/actions/workflows/build-ios-unsigned.yml) or Artifacts
2. Open **Feather** on your iPhone
3. Import and sign the IPA with your Apple ID
4. Done

## What's different from the official app

- Built as **unsigned IPA** for sideloading (no TestFlight/Plutonium needed)
- Share extension disabled (SPM dependency removed)
- Voice/video calls disabled (WebRTC removed)
- Push notifications work via APNs

## License

Same as the original project: [AGPLv3](LICENSE)

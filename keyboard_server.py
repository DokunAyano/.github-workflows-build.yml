# .github-workflows-build.yml
DroidBoard
name: Build APK and EXE

on:
  push:
  workflow_dispatch:

jobs:
  build-windows-exe:
    runs-on: windows-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install websockets pyautogui pyinstaller

      - name: Build EXE
        run: |
          pyinstaller --onefile --console keyboard_server.py

      - name: Upload EXE
        uses: actions/upload-artifact@v4
        with:
          name: Windows-Keyboard-Server-EXE
          path: dist/*.exe

  build-android-apk:
    if: ${{ hashFiles('gradlew') != '' }}
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up JDK 17
        uses: actions/setup-java@v4
        with:
          distribution: 'temurin'
          java-version: '17'

      - name: Make Gradle wrapper executable
        run: chmod +x gradlew

      - name: Build APK with Gradle
        run: ./gradlew assembleDebug

      - name: Upload APK
        uses: actions/upload-artifact@v4
        with:
          name: Android-Keyboard-APK
          path: app/build/outputs/apk/debug/*.apk

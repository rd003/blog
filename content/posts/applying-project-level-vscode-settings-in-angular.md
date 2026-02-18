+++
date = '2026-02-18T13:47:21+05:30'
draft = false
title = 'Applying Project Level Vscode Settings with Angular'
tags= ["angular"]
categories = ["programming"]
image = '/images/vscode-settings.webp'
+++

When you work with a team, everyone has their own preferences like double-quotes vs. single-quotes, trailing semicolon or not. If you want to decide a common code format that automatically applied. There are several ways which also comes with angular 21, like `prettier`. But you need to run the command for that every time. It is a nice feature. But you can also format code on file save. For that you need to follow these two steps.

1. Install ["prettier-formatter"](https://marketplace.visualstudio.com/items?itemName=esbenp.prettier-vscode) extension for vscode.

2. In root of the project create folder `.vscode`, inside this folder create `settings.json` file and paste the following content there:

```json
{
  "editor.formatOnSave": true,
  "editor.trimAutoWhitespace": true,
  "files.trimTrailingWhitespace": true,
  "prettier.singleQuote": true,
  "prettier.semi": true,
  "prettier.bracketSameLine": true,
  "[javascript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[typescript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  }
}
```

You need to adjust setting according to your preferences. Whenever you save the project, this setting will be applied.

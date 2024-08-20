#!/usr/bin/env bash
set -euo pipefail

git submodule update --init

mkdir -p "fonts"

mkdir -p "fonts/gen-ei-mono-go"
pushd "fonts/gen-ei-mono-go"
    if [[ ! -f "GenEiMonoGothic_v1.0.zip" ]]; then
        echo "You have to download \"GenEiMonoGothic_v1.0.zip\" manually."
        echo "https://okoneya.jp/font/genei-mono-go.html"
    else
        rm -rf ./*.ttf
        unzip -j "GenEiMonoGothic_v1.0.zip" "GenEiMonoGothic_v1.0/GenEiMonoGothic-*.ttf"
    fi
popd

mkdir -p "fonts/jetbrains-mono"
pushd "fonts/jetbrains-mono"
    rm -rf ./*
    wget -O "jetbrains-mono.zip" "https://github.com/JetBrains/JetBrainsMono/releases/download/v2.304/JetBrainsMono-2.304.zip"
    unzip -j "jetbrains-mono.zip" "fonts/ttf/*"
popd

mkdir -p "dist"
rm -rf "dist/*"

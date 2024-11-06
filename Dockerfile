# Use the existing Video2X image as the base
FROM ghcr.io/k4yt3x/video2x:latest

# Install git and vulkan-tools
RUN pacman -Sy --noconfirm git vulkan-tools && \
    rm -rf /var/cache/pacman/pkg/*

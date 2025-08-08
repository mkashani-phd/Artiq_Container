# syntax=docker/dockerfile:1.6
FROM ubuntu:20.04

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Etc/UTC LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8

# Base deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    tzdata curl sudo git gnupg xz-utils unzip locales ca-certificates \
    libncurses5 libtinfo5 libxi6 libxrender1 libxtst6 libxrandr2 libgtk2.0-0 \
    libcanberra-gtk-module libcanberra-gtk3-module && \
    rm -rf /var/lib/apt/lists/* && \
    locale-gen en_US.UTF-8

# Create non-root user (we'll use root only for the Vivado install step)
RUN useradd -m devuser && echo "devuser ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers
WORKDIR /home/devuser

# Nix as devuser
USER devuser
SHELL ["/bin/bash","-c"]
RUN curl -L https://nixos.org/nix/install | sh
ENV USER=devuser
ENV NIX_PATH=/home/devuser/.nix-defexpr/channels
ENV PATH=/home/devuser/.nix-profile/bin:/home/devuser/.nix-profile/sbin:$PATH
RUN . ~/.nix-profile/etc/profile.d/nix.sh || true

# Your generated config (make sure Destination=/opt/Xilinx)
COPY --chown=devuser install_config.txt /home/devuser/install_config.txt

# === Vivado install as root into /opt/Xilinx ===
USER root
# Ensure destination exists and is writable (installer usually requires root anyway)
RUN mkdir -p /opt/Xilinx && chown root:root /opt/Xilinx

# Mount the ALREADY-EXTRACTED installer dir, copy to /tmp (writable), run xsetup
RUN --mount=type=bind,from=installer,source=.,target=/mnt/xilinx,readonly \
    set -euo pipefail; \
    mkdir -p /tmp/xilinx; \
    srcdir="$(find /mnt/xilinx -maxdepth 2 -type f -name xsetup -printf '%h\n' | head -n1)"; \
    cp -a "$srcdir" /tmp/xilinx/installer; \
    chmod +x /tmp/xilinx/installer/xsetup; \
    /tmp/xilinx/installer/xsetup \
      -a XilinxEULA,3rdPartyEULA \
      -b Install \
      -c /home/devuser/install_config.txt; \
    rm -rf /tmp/xilinx

# Put Vivado on PATH for everyone
ENV PATH="/opt/Xilinx/Vivado/2022.2/bin:${PATH}"

# Back to devuser for normal use (Nix/ARTIQ, etc.)
USER devuser
WORKDIR /home/devuser
SHELL ["/bin/bash","-c"]

CMD ["bash"]

# syntax=docker/dockerfile:1.6

FROM ubuntu:20.04

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Etc/UTC LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8

# Base deps for Vivado + Nix (headless)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      tzdata curl sudo git gnupg xz-utils unzip locales ca-certificates \
      libncurses5 libtinfo5 libxi6 libxrender1 libxtst6 libxrandr2 libgtk2.0-0 \
      libcanberra-gtk-module libcanberra-gtk3-module && \
    rm -rf /var/lib/apt/lists/* && \
    locale-gen en_US.UTF-8

# Non-root user
RUN useradd -m devuser && echo "devuser ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers
USER devuser
WORKDIR /home/devuser
SHELL ["/bin/bash","-c"]

# Nix
RUN curl -L https://nixos.org/nix/install | sh
ENV USER=devuser
ENV NIX_PATH=/home/devuser/.nix-defexpr/channels
ENV PATH=/home/devuser/.nix-profile/bin:/home/devuser/.nix-profile/sbin:$PATH
RUN . ~/.nix-profile/etc/profile.d/nix.sh || true

# Copy ONLY the small config file (edit Destination below to /opt/Xilinx)
COPY --chown=devuser install_config.txt /home/devuser/install_config.txt

# Install Vivado by MOUNTING the huge tar for this step only (not added to the image)
RUN --mount=type=bind,from=installer,source=Xilinx_Unified_2022.2_1014_8888.tar.gz,target=/mnt/installer.tar.gz,readonly \
    mkdir -p /tmp/xilinx && \
    tar -xzf /mnt/installer.tar.gz -C /tmp/xilinx && \
    XSETUP=$(echo /tmp/xilinx/*/xsetup) && \
    chmod +x "$XSETUP" && \
    "$XSETUP" -a XilinxEULA,3rdPartyEULA -b Install -c /home/devuser/install_config.txt && \
    rm -rf /tmp/xilinx

# Vivado in PATH for ARTIQ
ENV PATH="/opt/Xilinx/Vivado/2022.2/bin:$PATH"

CMD ["bash"]


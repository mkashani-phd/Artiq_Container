FROM ubuntu:20.04

LABEL maintainer="mkashani.phd@gmail.com"


# ----- non-interactive apt -----
ARG DEBIAN_FRONTEND=noninteractive
ENV DEBIAN_FRONTEND=${DEBIAN_FRONTEND}
ENV TZ=Etc/UTC

# ----- deps for Vivado + Nix -----
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      tzdata \
      curl sudo git gnupg xz-utils unzip locales ca-certificates \
      libncurses5 libtinfo5 libxi6 libxrender1 libxtst6 libxrandr2 libgtk2.0-0 \
      libcanberra-gtk-module libcanberra-gtk3-module \
    && rm -rf /var/lib/apt/lists/*

# ----- locale -----
RUN locale-gen en_US.UTF-8
ENV LANG=en_US.UTF-8
ENV LANGUAGE=en_US:en
ENV LC_ALL=en_US.UTF-8

# ----- user -----
RUN useradd -m devuser && echo "devuser ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers
USER devuser
WORKDIR /home/devuser

# ----- Nix -----
RUN curl -L https://nixos.org/nix/install | sh
ENV USER=devuser
ENV NIX_PATH=/home/devuser/.nix-defexpr/channels
ENV PATH=/home/devuser/.nix-profile/bin:/home/devuser/.nix-profile/sbin:$PATH
SHELL ["/bin/bash", "-c"]
RUN . /home/devuser/.nix-profile/etc/profile.d/nix.sh || true

# ----- copy offline installer + config -----
# Place the tar.gz and install_config.txt beside this Dockerfile
COPY --chown=devuser Xilinx_Unified_2022.2_1014_8888.tar.gz .
COPY --chown=devuser install_config.txt .

# ----- extract & install Vivado to /opt/Xilinx -----
# The tar extracts a folder like Xilinx_Unified_2022.2_1014_8888/
RUN mkdir xilinx_offline && \
    tar -xzf Xilinx_Unified_2022.2_1014_8888.tar.gz -C xilinx_offline --strip-components=0 && \
    cd xilinx_offline && \
    ./xsetup \
      --batch Install \
      --agree XilinxEULA,3rdPartyEULA \
      --config ../install_config.txt && \
    cd .. && \
    rm -rf xilinx_offline Xilinx_Unified_2022.2_1014_8888.tar.gz

# ----- Vivado in PATH for ARTIQ -----
ENV PATH="/opt/Xilinx/Vivado/2022.2/bin:$PATH"

CMD ["bash"]

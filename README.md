# Making Artiq Container
The goal is to make a container that has the Artiq 7 and can be used to make gateware without having to install the Aritq and Vivado over and over for a new PC.

We are using Docker to make that container. First we install Docker and in the container we will install the Nix and Vivado and Artiq.

## Installing Docker
First download Docker from [here](https://desktop.docker.com/linux/main/amd64/docker-desktop-amd64.deb?utm_source=docker&utm_medium=webreferral&utm_campaign=docs-driven-download-linux-amd64&_gl=1*6uri53*_gcl_au*MTE4Nzg4ODY5Mi4xNzU0NTgxMDU3*_ga*MTYzNDk0MDMwOC4xNzU0NTc5OTYz*_ga_XJWPQMJYHQ*czE3NTQ1Nzk5NjMkbzEkZzEkdDE3NTQ1ODEwOTAkajE2JGwwJGgw) assuming you are using Ubuntu and the downloaded file is in Download folder. Then run the following commnands.

```bash
sudo apt install -y ca-certificates curl gnupg lsb-release
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt update -y
cd ~/Downloads

```
This line actually install the docker and hit enter to accept every question while runnign the following command.
```bash
sudo apt-get install ./docker-desktop-amd64.deb
```

Afer successful installation, we create a container with nix enviornment. 

## Creating NIX Container

to create a nix container we create a folder and create the Dockerfile

```bash
mkdir nix-container
cd nix-container
touch Dockerfile
```

Then paste the following in the Dockerfile and save.

```bash 
FROM ubuntu:22.04

LABEL maintainer="mkashani.phd@gmail.com"

# --------------------------
# Install system dependencies
# --------------------------
RUN apt-get update && apt-get install -y \
    curl sudo git gnupg xz-utils unzip locales \
    libncurses5 libtinfo5 libxi6 libxrender1 libxtst6 libxrandr2 libgtk2.0-0 \
    libcanberra-gtk-module libcanberra-gtk3-module \
    && rm -rf /var/lib/apt/lists/*

# --------------------------
# Set locale
# --------------------------
RUN locale-gen en_US.UTF-8
ENV LANG=en_US.UTF-8
ENV LANGUAGE=en_US:en
ENV LC_ALL=en_US.UTF-8

# --------------------------
# Create non-root user
# --------------------------
RUN useradd -m devuser && echo "devuser ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers
USER devuser
WORKDIR /home/devuser

# --------------------------
# Install Nix
# --------------------------
RUN curl -L https://nixos.org/nix/install | sh

ENV USER=devuser
ENV NIX_PATH=/home/devuser/.nix-defexpr/channels
ENV PATH=/home/devuser/.nix-profile/bin:/home/devuser/.nix-profile/sbin:$PATH

SHELL ["/bin/bash", "-c"]
RUN . /home/devuser/.nix-profile/etc/profile.d/nix.sh || true

# --------------------------
# Install Vivado
# --------------------------
# Copy your Vivado unified installer and config into image
COPY --chown=devuser Xilinx_Unified_2022.2_1014_8888_Lin64 .
COPY --chown=devuser install_config.txt .

# Make Vivado installer executable
RUN chmod +x Xilinx_Unified_2022.2_1014_8888_Lin64

# Run silent Vivado install into /opt/Xilinx
RUN ./Xilinx_Unified_2022.2_1014_8888_Lin64 \
    --batch Install \
    --agree XilinxEULA,3rdPartyEULA \
    --config install_config.txt

# Add Vivado to PATH (for ARTIQ compatibility)
ENV PATH="/opt/Xilinx/Vivado/2022.2/bin:$PATH"

CMD ["bash"]
```

To build the container run the following command

``` bash
docker build -t nix-env .
docker run -it nix-env
```

Now you are inside a Debian Linux container with Nix installed 🎉










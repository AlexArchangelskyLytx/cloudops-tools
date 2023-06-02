FROM ghcr.io/runatlantis/atlantis:v0.24.2

ENV ATLANTIS_CFG_VERSION=v1.16.0
ENV INFRACOST_VERSION=v0.10.17
ENV TERRAGRUNT_VERSION=v0.43.3
ENV TERRAMATE_VERSION=v0.2.12

RUN apk add --no-cache aws-cli vault
RUN setcap cap_ipc_lock= /usr/sbin/vault

# infracost
RUN curl -s -L https://github.com/infracost/infracost/releases/download/${INFRACOST_VERSION}/infracost-linux-amd64.tar.gz | tar xz -C /tmp && \
    mv /tmp/infracost-linux-amd64 /usr/bin/infracost

# terragrunt
RUN curl -s -Lo terragrunt https://github.com/gruntwork-io/terragrunt/releases/download/${TERRAGRUNT_VERSION}/terragrunt_linux_amd64 && \
    chmod +x terragrunt && mv terragrunt /usr/local/bin

# terragrunt-atlantis-config
RUN curl -s -L "https://github.com/transcend-io/terragrunt-atlantis-config/releases/download/${ATLANTIS_CFG_VERSION}/terragrunt-atlantis-config_${ATLANTIS_CFG_VERSION#v}_linux_amd64.tar.gz" | tar xz -C /tmp && \
    mv "/tmp/terragrunt-atlantis-config_${ATLANTIS_CFG_VERSION#v}_linux_amd64/terragrunt-atlantis-config_${ATLANTIS_CFG_VERSION#v}_linux_amd64" /usr/bin/terragrunt-atlantis-config

# terramate
RUN curl -s -L "https://github.com/mineiros-io/terramate/releases/download/${TERRAMATE_VERSION}/terramate_${TERRAMATE_VERSION#v}_linux_x86_64.tar.gz"  | tar xz -C /tmp && \
    mv /tmp/terramate /usr/bin/terramate

# Prepare the plugin cache directory ahead of time
RUN mkdir -p /plugins && chown -R atlantis:atlantis /plugins
RUN mkdir -p /home/atlantis/.ssh && chown -R atlantis:atlantis /home/atlantis/.ssh

RUN rm -rf /tmp/*

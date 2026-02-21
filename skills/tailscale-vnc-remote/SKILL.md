---
name: tailscale-vnc-remote
description: Setup Tailscale VPN and VNC remote desktop access for secure remote connections. Use when configuring remote desktop access via Tailscale VPN, setting up VNC server with proper user authentication, or creating secure headless/remote access to Raspberry Pi or Linux workstations. Supports RealVNC Server with user-mode sessions and Tailscale integration for secure connectivity without port forwarding.
---

# Tailscale + VNC Remote Access Setup

This skill configures secure remote desktop access using Tailscale VPN and RealVNC Server.

## Overview

- **Tailscale** creates a secure mesh VPN (tailnet) between devices
- **RealVNC Server** provides virtual desktop sessions
- **Combined**: Secure remote access without port forwarding or firewall rules

## Prerequisites

- Debian/Ubuntu/Raspberry Pi OS
- RealVNC Server (usually pre-installed on Raspberry Pi)
- Root/sudo access

## Quick Setup Workflow

### 1. Install Tailscale

```bash
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up
```

**Note**: User must authenticate via provided URL.

### 2. Configure RealVNC Server for User Mode

Stop system service if running:
```bash
sudo systemctl stop vncserver-virtuald.service
sudo systemctl disable vncserver-virtuald.service
```

Set VNC password for user:
```bash
vncpasswd -virtual
# Enter password (min 6 chars)
```

### 3. Create User Service

Create `/etc/systemd/system/vnc-<user>.service`:

```ini
[Unit]
Description=VNC Server (Virtual Mode) for <user>
After=network.target

[Service]
Type=forking
User=<user>
Group=<user>
WorkingDirectory=/home/<user>
Environment=HOME=/home/<user>
Environment=USER=<user>
ExecStart=/usr/bin/vncserver-virtual :1 -Authentication VncAuth
ExecStop=/usr/bin/vncserver-virtual -kill :1
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable vnc-<user>.service
sudo systemctl start vnc-<user>.service
```

### 4. Verify Setup

```bash
# Check Tailscale IP
tailscale status

# Check VNC is listening
ss -tlnp | grep 5901

# Check service status
sudo systemctl status vnc-<user>.service
```

## Connection Details

| Setting | Value |
|---------|-------|
| Address | `<tailscale-ip>:5901` |
| Auth | VncAuth (password) |
| Display | `:1` |

## Troubleshooting

### Authentication Failed
- Ensure `-Authentication VncAuth` is set
- Verify password with `vncpasswd -virtual`

### Cannot Connect
- Check Tailscale status: `tailscale status`
- Verify VNC port: `ss -tlnp | grep 5901`
- Check firewall: `sudo ufw status`

### Service Won't Start
- Check logs: `sudo journalctl -u vnc-<user>.service -n 50`
- Verify user exists and has home directory
- Ensure `vncpasswd` was run as target user

## Scripts

Use `scripts/setup-tailscale-vnc.sh` for automated setup. See script comments for usage.

## References

- `references/SETUP-GUIDE.md` - Detailed setup instructions with screenshots

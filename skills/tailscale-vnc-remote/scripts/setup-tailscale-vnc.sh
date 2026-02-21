#!/bin/bash
#
# Setup Tailscale + VNC Remote Access
# Usage: sudo ./setup-tailscale-vnc.sh [username] [vnc_password]
#

set -e

USERNAME="${1:-$SUDO_USER}"
VNC_PASS="${2:-}"

if [ -z "$USERNAME" ]; then
    echo "Error: Could not determine username"
    echo "Usage: sudo ./setup-tailscale-vnc.sh <username> [vnc_password]"
    exit 1
fi

if [ "$EUID" -ne 0 ]; then
    echo "Error: Please run as root or with sudo"
    exit 1
fi

echo "=== Tailscale + VNC Setup ==="
echo "User: $USERNAME"
echo ""

# Check if Tailscale is installed
if ! command -v tailscale &> /dev/null; then
    echo "[1/5] Installing Tailscale..."
    curl -fsSL https://tailscale.com/install.sh | sh
else
    echo "[1/5] Tailscale already installed"
fi

# Check Tailscale status
echo "[2/5] Checking Tailscale status..."
if ! tailscale status &> /dev/null; then
    echo "Starting Tailscale authentication..."
    echo "Please authenticate using the URL that will appear below:"
    tailscale up
else
    echo "Tailscale already authenticated"
    tailscale status | grep "$(hostname)"
fi

# Install RealVNC if not present
if ! command -v vncserver-virtual &> /dev/null; then
    echo "[3/5] Installing RealVNC Server..."
    apt-get update
    apt-get install -y realvnc-vnc-server
else
    echo "[3/5] RealVNC Server already installed"
fi

# Stop/disable root VNC service
echo "[4/5] Stopping root VNC service..."
systemctl stop vncserver-virtuald.service 2>/dev/null || true
systemctl disable vncserver-virtuald.service 2>/dev/null || true

# Set VNC password for user
echo "[5/5] Configuring VNC for user $USERNAME..."
if [ -n "$VNC_PASS" ]; then
    # Set password non-interactively
    echo -e "${VNC_PASS}\n${VNC_PASS}" | su - "$USERNAME" -c "vncpasswd -virtual" 2>/dev/null || {
        echo "Warning: Could not set password automatically"
        echo "Please run manually as $USERNAME: vncpasswd -virtual"
    }
else
    echo "No password provided. Please set manually as $USERNAME:"
    echo "  vncpasswd -virtual"
fi

# Create systemd service
SERVICE_FILE="/etc/systemd/system/vnc-${USERNAME}.service"
cat > "$SERVICE_FILE" << EOF
[Unit]
Description=VNC Server (Virtual Mode) for $USERNAME
After=network.target

[Service]
Type=forking
User=$USERNAME
Group=$USERNAME
WorkingDirectory=/home/$USERNAME
Environment=HOME=/home/$USERNAME
Environment=USER=$USERNAME
ExecStart=/usr/bin/vncserver-virtual :1 -Authentication VncAuth
ExecStop=/usr/bin/vncserver-virtual -kill :1
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

# Reload and start service
systemctl daemon-reload
systemctl enable "vnc-${USERNAME}.service"
systemctl restart "vnc-${USERNAME}.service"

# Wait for service to start
sleep 2

# Verify
echo ""
echo "=== Setup Complete ==="
echo ""
echo "Tailscale IP:"
tailscale status | grep "$(hostname)" | awk '{print $1}'
echo ""
echo "VNC Status:"
if systemctl is-active --quiet "vnc-${USERNAME}.service"; then
    echo "  ✓ VNC service running"
    ss -tlnp | grep 5901 | head -1
else
    echo "  ✗ VNC service failed to start"
    echo "  Check: sudo journalctl -u vnc-${USERNAME}.service -n 20"
fi
echo ""
echo "Connection details:"
echo "  Address: <tailscale-ip>:5901"
echo "  Password: (set during vncpasswd)"

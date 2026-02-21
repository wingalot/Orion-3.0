# Tailscale + VNC Remote Access - Setup Guide

## Kam tas domāts

Šis skill ļauj droši pieslēgties Raspberry Pi vai Linux darbstacijai attālināti no jebkuras vietas, izmantojot Tailscale VPN un VNC.

**Galvenās priekšrocības:**
- Nav vajadzīgs port forwarding
- Nav jāatver porti routerī
- Šifrēts savienojums
- Strādā pat aiz NAT/firewall

---

## Priekšnoteikumi

- Raspberry Pi vai Linux dators ar GUI (X11/Wayland)
- Debian/Ubuntu/Raspberry Pi OS
- Interneta pieslēgums
- Root/sudo piekļuve

---

## Iestatīšanas soļi

### 1. Instalēt Tailscale

```bash
curl -fsSL https://tailscale.com/install.sh | sh
```

Pēc instalācijas jāautentificējas:
```bash
sudo tailscale up
```

Tiks parādīts kods un saite (`https://login.tailscale.com/a/...`). Atver to pārlūkā un pieslēdzies ar Google/Microsoft/GitHub kontu.

Pārbaudi statusu:
```bash
tailscale status
```

Redzēsi savu ierīces IP (piemēram, `100.x.x.x`).

---

### 2. Pārbaudīt RealVNC Server

Parasti jau instalēts Raspberry Pi:
```bash
which vncserver-virtual
```

Ja nav instalēts:
```bash
sudo apt-get update
sudo apt-get install -y realvnc-vnc-server
```

---

### 3. Iestatīt VNC paroli

Kā lietotājs (ne root!):
```bash
vncpasswd -virtual
```

Ievadi paroli (vismaz 6 simboli).

---

### 4. Izveidot systemd servisu

Izveido failu `/etc/systemd/system/vnc-TAVS_LIETOTĀJS.service`:

```ini
[Unit]
Description=VNC Server (Virtual Mode) for TAVS_LIETOTĀJS
After=network.target

[Service]
Type=forking
User=TAVS_LIETOTĀJS
Group=TAVS_LIETOTĀJS
WorkingDirectory=/home/TAVS_LIETOTĀJS
Environment=HOME=/home/TAVS_LIETOTĀJS
Environment=USER=TAVS_LIETOTĀJS
ExecStart=/usr/bin/vncserver-virtual :1 -Authentication VncAuth
ExecStop=/usr/bin/vncserver-virtual -kill :1
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
```

**Svarīgi:** Aizstāj `TAVS_LIETOTĀJS` ar savu lietotājvārdu!

---

### 5. Iespējot un palaist servisu

```bash
sudo systemctl daemon-reload
sudo systemctl enable vnc-TAVS_LIETOTĀJS.service
sudo systemctl start vnc-TAVS_LIETOTĀJS.service
```

Pārbaudi statusu:
```bash
sudo systemctl status vnc-TAVS_LIETOTĀJS.service
```

---

### 6. Pārbaudīt portu

```bash
ss -tlnp | grep 5901
```

Jāredz kaut kas līdzīgs:
```
LISTEN 0 5 0.0.0.0:5901 ...
```

---

## Pieslēgšanās

### No cita datora/telefona

1. Instalē Tailscale uz ierīces, no kuras pieslēgsies
2. Pieslēdzies tai pašai tailnet (kontam)
3. Atver VNC Viewer:
   - **Adrese**: `100.x.x.x:5901` (Tailscale IP)
   - **Parole**: tā, kas iestatīta ar `vncpasswd`

### Ieteicamie VNC klienti

- **Desktop**: RealVNC Viewer, TigerVNC Viewer
- **Android/iOS**: RealVNC Viewer app
- **Web**: `https://100.x.x.x:5900` (ja iespējots)

---

## Problēmu risināšana

### "Username not recognised" kļūda

RealVNC pēc noklusējuma mēģina izmantot sistēmas autentifikāciju. Pievieno servisa failā:
```
ExecStart=/usr/bin/vncserver-virtual :1 -Authentication VncAuth
```

### Serviss nestartējas

Pārbaudi žurnālus:
```bash
sudo journalctl -u vnc-TAVS_LIETOTĀJS.service -n 50
```

Biežākie iemesli:
- Nav iestatīta VNC parole
- Lietotājam nav mājas direktorijas
- Cits process jau izmanto portu 5901

### Tailscale neiet

Pārbaudi:
```bash
sudo systemctl status tailscaled
sudo tailscale status
```

Ja nav autentificēts:
```bash
sudo tailscale up
```

### VNC paroles aizmiršana

Iestati jaunu:
```bash
vncpasswd -virtual
```

Un pārstartē servisu:
```bash
sudo systemctl restart vnc-TAVS_LIETOTĀJS.service
```

---

## Drošības ieteikumi

1. **Nekad neatstāj noklusējuma paroli** — iestati stipru VNC paroli
2. **Ierobežo Tailscale piekļuvi** — izmanto ACL, lai ierobežotu, kuras ierīces var sasniegt tavu Pi
3. **Atjaunini regulāri**:
   ```bash
   sudo apt-get update && sudo apt-get upgrade
   ```
4. **Ieslēdz automātiskos atjauninājumus** Tailscale:
   ```bash
   sudo tailscale set --auto-update
   ```

---

## Automātiskā iestatīšana

Izmanto skriptu `scripts/setup-tailscale-vnc.sh`:

```bash
sudo ./setup-tailscale-vnc.sh lietotājs parole
```

Vai bez paroles (būs jāievada manuāli):
```bash
sudo ./setup-tailscale-vnc.sh lietotājs
```

---

## Papildu konfigurācija

### Mainīt VNC portu

Servisa failā maini `:1` uz citu displeju:
- `:1` = ports 5901
- `:2` = ports 5902
- `:0` = ports 5900

### Piekļuve tikai no noteiktām IP

Tailscale ACL (Admin Console → Access Controls):
```json
{
  "acls": [
    {
      "action": "accept",
      "src": ["tag:trusted"],
      "dst": ["100.x.x.x:5901"]
    }
  ]
}
```

---

## Resursi

- Tailscale dokumentācija: https://tailscale.com/kb
- RealVNC dokumentācija: https://www.realvnc.com/docs/
- Raspberry Pi VNC: https://www.raspberrypi.com/documentation/computers/remote-access.html

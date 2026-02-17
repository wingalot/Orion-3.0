# SSH Savienojums Starp Raspberry Pi Iekārtām

> Instrukcijas Oreo un Kimi — kā droši savienot divas Raspberry Pi iekārtas caur SSH.

---

## 🎯 Kas Nepieciešams

- Divas Raspberry Pi iekārtas ar OS (Raspberry Pi OS/Ubuntu/Debian)
- Tīkla savienojums (LAN vai WiFi)
- Lietotāju konti uz abām iekārtām

---

## 📋 Iekārtu Identifikācija

| Iekārta | Loma | Hostname (parasts) | Lietotājs |
|---------|------|-------------------|-----------|
| Pi 1 | Serveris (mērķis) | `raspberrypi` vai `kimi` | `pi` vai `oreo` |
| Pi 2 | Klients (kurš savienojas) | `raspberrypi2` vai `oreo` | `pi` vai `oreo` |

> **Note:** Hostnames jābūt unikāliem tīklā! Pārbaudi ar `hostname` un maini ar `sudo hostnamectl set-hostname <jauns-vards>`

---

## 1️⃣ Tīkla Pārbaude

### Atrast IP adreses

Uz **servera** (mērķa Pi):
```bash
hostname -I
# vai
ip addr show
```

Parasti izskatās: `192.168.1.XXX` vai `10.0.0.XXX`

### Ping tests no klienta

```bash
ping <servera-ip>
# Piemēram:
ping 192.168.1.50
```

---

## 2️⃣ SSH Servera Uzstādīšana (Uz Mērķa Pi)

### Pārbaudīt vai SSH ir aktīvs

```bash
sudo systemctl status ssh
```

### Ja nav aktīvs — ieslēgt

```bash
sudo apt update
sudo apt install openssh-server
sudo systemctl enable ssh
sudo systemctl start ssh
```

### Pārbaudīt portu

```bash
sudo ss -tlnp | grep ssh
# Vai
telnet localhost 22
```

---

## 3️⃣ SSH Key Autentifikācija (Ieteicams)

### 3.1 Ģenerēt SSH atslēgu pārī klientā

```bash
ssh-keygen -t ed25519 -C "oreo@raspberrypi"
# Vai vecākām sistēmām:
ssh-keygen -t rsa -b 4096 -C "oreo@raspberrypi"
```

> **Piezīme:** Passphrase ir opcionāla. Tukša = automātiska pieslēgšanās.

Atslēgas atrašanās vieta:
- Privātā: `~/.ssh/id_ed25519` **(NEKAD NEKOPĒT!)**
- Publiskā: `~/.ssh/id_ed25519.pub` ✅ (droši kopēt)

### 3.2 Kopēt publisko atslēgu uz serveri

**Metode A: ssh-copy-id (vienkāršākā)**
```bash
ssh-copy-id lietotajs@servera-ip
# Piemēram:
ssh-copy-id oreo@192.168.1.50
```

**Metode B: Manuāli**
```bash
cat ~/.ssh/id_ed25519.pub | ssh lietotajs@servera-ip "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"
```

### 3.3 Pārbaude

```bash
ssh oreo@192.168.1.50
# Ja viss OK — iekļūsi bez paroles
```

---

## 4️⃣ SSH Config Fails (Ērtībai)

Uz **klienta** izveidot `~/.ssh/config`:

```bash
nano ~/.ssh/config
```

Pievienot:
```
Host kimi
    HostName 192.168.1.50
    User oreo
    IdentityFile ~/.ssh/id_ed25519
    Port 22

Host oreo-pi
    HostName 192.168.1.51
    User pi
    IdentityFile ~/.ssh/id_ed25519
```

Tagad vari vienkārši:
```bash
ssh kimi
ssh oreo-pi
```

---

## 5️⃣ Drošības Iestatījumi (Ieteicams)

Uz **servera** rediģēt `/etc/ssh/sshd_config`:

```bash
sudo nano /etc/ssh/sshd_config
```

Ieteicamie iestatījumi:
```
# Aizliegt root pieslēgšanos
PermitRootLogin no

# Atļaut tikai atslēgu autentifikāciju
PasswordAuthentication no
PubkeyAuthentication yes

# Mainīt portu (neobligāti)
# Port 2222

# Ierobežot lietotājus
AllowUsers oreo pi
```

Pārlādēt SSH:
```bash
sudo systemctl restart ssh
```

---

## 6️⃣ SSH Agent (Atslēgu Pārvalde)

Automātiska atslēgu ielāde:

```bash
# Pievienot atslēgu agentam
ssh-add ~/.ssh/id_ed25519

# Pārbaudīt kādas atslēgas ir ielādētas
ssh-add -l
```

Auto-start bashrc:
```bash
echo 'eval "$(ssh-agent -s)"' >> ~/.bashrc
echo 'ssh-add ~/.ssh/id_ed25519' >> ~/.bashrc
```

---

## 🔧 Diagnostika

### Savienojums nestrādā?

```bash
# Detalizēts logs
ssh -v oreo@192.168.1.50
ssh -vv oreo@192.168.1.50  # vēl detalizētāk

# Pārbaudīt vai ports ir atvērts
nc -zv 192.168.1.50 22

# Pārbaudīt firewall
sudo ufw status
sudo iptables -L | grep 22
```

### SSH config pārbaude

```bash
ssh -G kimi
# Parāda pilnu konfigurāciju hostam
```

### Log faili

```bash
sudo tail -f /var/log/auth.log
```

---

## 📁 Svarīgākie Faili un Lokācijas

| Fails | Lokācija | Nozīme |
|-------|----------|--------|
| Privātā atslēga | `~/.ssh/id_ed25519` | **NEKAD NEKOPĒT!** |
| Publiskā atslēga | `~/.ssh/id_ed25519.pub` | Droši kopēt uz serveriem |
| Autorizētās atslēgas | `~/.ssh/authorized_keys` | Servera pusē — kas drīkst iekļūt |
| SSH konfigs | `~/.ssh/config` | Klienta īsceļi |
| SSH daemon config | `/etc/ssh/sshd_config` | Servera iestatījumi |

---

## 🚀 Ātrās Komandas

```bash
# Pieslēgties
ssh oreo@192.168.1.50

# Ar portu (ja mainīts)
ssh -p 2222 oreo@192.168.1.50

# Ar konkrētu atslēgu
ssh -i ~/.ssh/mana_atslega oreo@192.168.1.50

# Kaut ko izpildīt un atvienoties
ssh oreo@192.168.1.50 "ls -la /home"

# Kopēt failus (SCP)
scp fails.txt oreo@192.168.1.50:/home/oreo/

# Kopēt atpakaļ
scp oreo@192.168.1.50:/home/oreo/fails.txt ./

# SSH ar X11 forwarding (grafiskās lietotnes)
ssh -X oreo@192.168.1.50
```

---

## ⚠️ Bezpeizības Noteikumi

1. **NEKAD** nepublicēt `~/.ssh/id_ed25519` (privātā atslēga)
2. **NEKAD** necommitot SSH atslēgas GitHub
3. `.ssh` mapei jābūt `chmod 700`
4. `authorized_keys` failam jābūt `chmod 600`
5. Pirms `PasswordAuthentication no` pārliecinies ka atslēga strādā!

---

## 📝 Piemērs: Divu Pi Setup

**Oreo (Klienta Pi):**
- IP: `192.168.1.100`
- Hostname: `oreo`
- Lietotājs: `pi`

**Kimi (Servera Pi):**
- IP: `192.168.1.101`
- Hostname: `kimi`
- Lietotājs: `pi`

**Soļi:**
1. Kimi: `sudo apt install openssh-server && sudo systemctl enable ssh`
2. Oreo: `ssh-keygen -t ed25519`
3. Oreo: `ssh-copy-id pi@192.168.1.101`
4. Oreo: `ssh pi@192.168.1.101` ✅

---

*Izveidots: 2024-02-17*
*Autors: Oreo & Kimi 🤖🦝*

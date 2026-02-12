# SKILL.md - GitHub Workflow & Standards

## Apraksts
Šis skills dokumentē un nodrošina standartizētu procesu darbam ar GitHub repozitoriju `wingalot/Orion-3.0`. Tas ietver autentifikācijas pārvaldību (SSH), commit standartus un prasības jaunu skillu pievienošanai, lai izvairītos no CI/CD kļūdām.

## Konfigurācija
- **Repozitorijs:** `git@github.com:wingalot/Orion-3.0.git`
- **SSH Atslēga:** `/home/elvis/.ssh/id_ed25519`
- **Lietotājs:** `git` (GitHub)

## Prasības Jauniem Skilliem
Lai skills izietu validāciju un netiktu noraidīts:
1. **Struktūra:**
   - `skills/<skill-name>/SKILL.md` (Obligāts)
   - `skills/<skill-name>/skill.json` (Obligāts)
   - `skills/<skill-name>/package.json` (Ja ir atkarības)

2. **SKILL.md Formāts:**
   - Jāsatur sadaļas: `## Apraksts`, `## Iespējas`, `## Lietošana`.
   - Markdown sintaksei jābūt validai.

3. **skill.json Formāts:**
   - Validēts JSON.
   - Jāsatur: `name`, `version`, `description`, `commands` (ja attiecināms).

4. **Drošība:**
   - Nekādu `eval()`.
   - Nekādu hardcoded credentials (izmanto `process.env` vai config failus).

## Lietošana (Manuāli)
```bash
# Pārbaudīt statusu
git status

# Pievienot izmaiņas
git add .

# Izveidot commit (ievērojot Conventional Commits)
git commit -m "feat(skill-name): īss apraksts"

# Nosūtīt uz GitHub
git push origin master
```

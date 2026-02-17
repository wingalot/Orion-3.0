#!/bin/bash
# Oreo Backup Script
# Ērti palaižams backup skripts

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_DIR="$HOME/.openclaw/workspace"
SKILLS_DIR="$WORKSPACE_DIR/orion-skills/skills"

# Krāsas (ANSI escape codes)
GREEN=$'\033[0;32m'
BLUE=$'\033[0;34m'
YELLOW=$'\033[1;33m'
RED=$'\033[0;31m'
NC=$'\033[0m' # No Color

show_help() {
    echo -e "${BLUE}Oreo Backup Tool${NC}"
    echo ""
    echo "Lietošana:"
    echo "  $(basename $0) [komanda] [opcijas]"
    echo ""
    echo "Komandas:"
    echo "  create    Izveidot jaunu backup"
    echo "  restore   Atjaunot no backup"
    echo "  list      Parādīt pieejamos backup failus"
    echo "  cleanup   Dzēst vecos backup failus"
    echo "  help      Parādīt šo palīdzību"
    echo ""
    echo "Opcijas:"
    echo "  --name    Backup nosaukums (create)"
    echo "  --force   Automātiskā atjaunošana (restore)"
    echo "  --keep    Saglabājamo failu skaits (cleanup)"
    echo ""
    echo "Piemēri:"
    echo "  $(basename $0) create                    # Izveidot backup"
    echo "  $(basename $0) create --name pirms-labojuma"
    echo "  $(basename $0) restore                   # Interaktīvā atjaunošana"
    echo "  $(basename $0) restore --force           # Ātrā atjaunošana"
    echo "  $(basename $0) list                      # Saraksts"
    echo "  $(basename $0) cleanup --keep 5          # Dzēst vecos"
}

create_backup() {
    echo -e "${GREEN}🚀 Izveidoju Oreo backup...${NC}"
    cd "$WORKSPACE_DIR"
    node "$SKILLS_DIR/backup-manager/create.js" "$@"
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Backup veiksmīgi izveidots!${NC}"
    else
        echo -e "${RED}❌ Backup izveide neizdevās${NC}"
        exit 1
    fi
}

restore_backup() {
    echo -e "${YELLOW}🔄 Atjaunoju Oreo no backup...${NC}"
    cd "$WORKSPACE_DIR"
    node "$SKILLS_DIR/restore-backup/restore.js" "$@"
}

list_backups() {
    BACKUP_DIR="${HOME}/oreo/backups"
    if [ ! -d "$BACKUP_DIR" ]; then
        BACKUP_DIR="/home/oreo/backups"
    fi
    
    echo -e "${BLUE}📦 Pieejamie backup faili:${NC}"
    echo ""
    
    if [ ! -d "$BACKUP_DIR" ]; then
        echo -e "${RED}❌ Backup mape neeksistē: $BACKUP_DIR${NC}"
        exit 1
    fi
    
    # Saraksts ar izmēriem
    ls -lh "$BACKUP_DIR"/*.tar.gz 2>/dev/null | awk '
    {
        printf "  %-10s %-8s %-10s %-5s %s\n", $6, $7, $8, $9, $10
    }' || echo "  Nav atrasts neviens backup fails"
    
    echo ""
    echo -e "${BLUE}📍 Atrašanās vieta: $BACKUP_DIR${NC}"
}

cleanup_backups() {
    echo -e "${YELLOW}🧹 Tīru vecos backup failus...${NC}"
    cd "$WORKSPACE_DIR"
    node "$SKILLS_DIR/backup-manager/cleanup.js" "$@"
}

# Galvenā loģika
case "${1:-help}" in
    create)
        shift
        create_backup "$@"
        ;;
    restore)
        shift
        restore_backup "$@"
        ;;
    list|ls)
        list_backups
        ;;
    cleanup|clean)
        shift
        cleanup_backups "$@"
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo -e "${RED}Nezināma komanda: $1${NC}"
        echo "Izmantojiet 'help' lai redzētu pieejamās komandas"
        exit 1
        ;;
esac

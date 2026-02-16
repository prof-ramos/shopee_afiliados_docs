<!-- Parent: ../AGENTS.md -->
<!-- Generated: 2026-02-15 | Updated: 2026-02-15 -->

# archive

## Purpose
Arquivos arquivados do projeto. Contém versões antigas, logs de organização e scripts de desfazer mudanças.

## Key Files

| File | Description |
|------|-------------|
| `ORGANIZATION_LOG_2026-02-12.md` | Log detalhado da reorganização do projeto |
| `undo_organization_2026-02-12.sh` | Script para reverter alterações de organização |

## Subdirectories

| Directory | Purpose |
|-----------|---------|
| `old/` | Arquivos antigos movidos durante reorganização |

## For AI Agents

### Working In This Directory
- Arquivos aqui são mantidos para referência histórica
- Use `ORGANIZATION_LOG_*.md` para entender mudanças passadas
- O script `undo_organization_*.sh` pode reverter alterações se necessário

### Organization Log
O log de 2026-02-12 documenta:
- Reestruturação de diretórios
- Movimentação de arquivos
- Criação de nova organização
- Decisões tomadas durante o processo

### Undo Script
Script bash que pode reverter a organização:
```bash
bash archive/undo_organization_2026-02-12.sh
```

⚠️ **Cuidado**: Executar o script undo pode alterar a estrutura atual do projeto.

### Common Patterns
- Arquivos são nomeados com timestamp para rastreabilidade
- Scripts undo correspondem aos logs de organização
- Mantenha arquivos aqui por pelo menos 30 dias antes de deletar

## Dependencies

### Internal
- Diretório raiz do projeto para reverter alterações

### External
- `bash` - Para executar scripts de undo

<!-- MANUAL: -->
